# coding: utf-8

"""
MIT License

Copyright (c) 2018 Veikko Kovanen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pandas as pd
from dateutil import parser
from datetime import datetime, timedelta
from sklearn import model_selection, preprocessing, ensemble

# data parameters
categorical_columns = ["vehicle_type", "location_id", "direction", "weekday", "week"]
dependent_columns = ["hour_{}".format(n) for n in range(1,25)]

# functions
def to_train_format(raw_data):
    """
    Converts categorical fields to dummies (and normalizes the values).
    Returns a DataFrame.
    """
    data = raw_data
    for col in categorical_columns:
        dummies = pd.get_dummies(data[col], prefix=col)
        data = pd.concat([data, dummies], axis=1)
        data = data.drop([col], axis=1)
    return data

def train_test_split(data, test_size=0.20):
    """
    Splits the formatted data into train and test sets.
    Returns X and Y + associated test sets as DataFrames.
    """
    X = data.drop(dependent_columns, axis=1)
    Y = data[dependent_columns]
    X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size)
    return X_train, X_test, Y_train, Y_test

def train(X_train, Y_train, model):
    """
    Fits the model to the train data.
    Modifies the model parameter.
    """
    model.fit(X_train, Y_train)
    model.features = X_train.columns
    model.targets = Y_train.columns

def evaluate(X_test, Y_test, model):
    """
    Returns the coefficient of determination R^2 of the prediction.
    """
    score = model.score(X_test, Y_test)
    return score

def evaluate_target_period():
    return

def predict(row, model):
    """
    Uses the trained model to predict with the given DataFrame.
    Returns a DataFrame including the predictions.
    """
    row_f = to_train_format(row)
    row_formatted = pd.DataFrame()
    for col in model.features:
        if col in row_f.columns:
            row_formatted[col] = row_f[col]
        else:
            row_formatted[col] = 0
    pred = pd.DataFrame(model.predict(row_formatted))
    pred.columns = model.targets
    return pred

def sample_prediction(sample_data, model):
    """
    Generates the prediction of a sample item.
    Returns a DataFrame containing the original and the
    predicted values side-by-side.
    """
    sample = sample_data.sample(1)
    result = pd.concat([sample, predict(sample, model)]).fillna("").transpose()
    index = result.columns[0]
    result.columns = [index, "prediction"]
    return result

def generate_prediction_series(model, dates, location_ids, vehicle_types):
    """
    Generates a predicted data series for the given dates,
    locations, and vehicle types. Returns a DataFrame.
    """
    generated = pd.DataFrame()
    for date_str in dates:
        date = parser.parse(date_str)
        for location_id in location_ids:
            for vehicle_type in vehicle_types:
                for direction in [1,2]:
                    row = pd.DataFrame()
                    row["year"] = [date.year]
                    row["week"] = [date.isocalendar()[1]]
                    row["weekday"] = [date.weekday()]
                    row["location_id"] = [location_id]
                    row["direction"] = [direction]
                    row["vehicle_type"] = [vehicle_type]
                    prediction = predict(row, model)
                    prediction.columns = dependent_columns
                    combined = pd.concat([row, prediction], axis=1)
                    generated = generated.append(combined, ignore_index=True)
    return generated

def get_location_name(location_id):
    """
    Returns the LAM station name of a location_id.
    """
    names = {168: "Askisto", 1403: "Kemijärvi", 110: "Mäntsälä"}
    return names[location_id]

def get_ts_row(data, location_id, year, week, weekday, hour):
    """
    Returns time series formatted row from the data. Includes only Cars & Vans, Trucs and Buses.
    """
    ts_row = pd.DataFrame()
    rows = data[(data.location_id == location_id) & (data.year == year) & (data.week == week) & (data.weekday == weekday)]
    cars_1 = rows[(rows.vehicle_type == "11 HA-PA") & (rows.direction == 1)]["hour_{}".format(hour)].iloc[0]
    cars_2 = rows[(rows.vehicle_type == "11 HA-PA") & (rows.direction == 2)]["hour_{}".format(hour)].iloc[0]
    trucks_1 = rows[(rows.vehicle_type == "12 KAIP") & (rows.direction == 1)]["hour_{}".format(hour)].iloc[0]
    trucks_2 = rows[(rows.vehicle_type == "12 KAIP") & (rows.direction == 2)]["hour_{}".format(hour)].iloc[0]
    buses_1 = rows[(rows.vehicle_type == "13 Linja-autot") & (rows.direction == 1)]["hour_{}".format(hour)].iloc[0]
    buses_2 = rows[(rows.vehicle_type == "13 Linja-autot") & (rows.direction == 2)]["hour_{}".format(hour)].iloc[0]
    date = datetime.strptime("{}-{}-{}".format(year, week, weekday+1), "%Y-%W-%u")
    ts_row["date"] = [date]
    ts_row["hour"] = "{:02}-{:02}".format(hour-1, hour)
    ts_row["LAM Station"] = [get_location_name(location_id)]
    ts_row["Cars and Vans - 1"] = cars_1
    ts_row["Cars and Vans - 2"] = cars_2
    ts_row["Trucks - 1"] = trucks_1
    ts_row["Trucks - 2"] = trucks_2
    ts_row["Buses - 1"] = buses_1
    ts_row["Buses - 2"] = buses_2
    return ts_row

def to_ts_format(data):
    """
    Converts the given dataset (of training or generating format)
    to time series format. Returns a DataFrame.
    """
    ts_data = pd.DataFrame()
    for location_id in data.location_id.unique():
        for year in data[data.location_id == location_id].year.unique():
            for week in data[(data.location_id == location_id) & (data.year == year)].week.unique():
                for weekday in data[(data.location_id == location_id) & (data.year == year) & (data.week == week)].weekday.unique():
                    for hour in range(1,25):
                        try:
                            row = get_ts_row(data, location_id, year, week, weekday, hour)
                            ts_data = pd.concat([ts_data, row])
                        except (ValueError, IndexError) as error:
                            print("Failed: ", location_id, year, week, weekday, hour)
                            print(error)
    return ts_data.reset_index(drop=True)


# split the raw data to train and test sets
print("Importing raw data...")
raw_data = pd.read_csv("refined_dataset.csv").sort_values(by="date")
raw_data = raw_data.drop(["sum", "location_name", "date"], axis=1)
model_data = raw_data
print("Reformatting data...")
train_formatted_data = to_train_format(model_data)
X_train, X_test, Y_train, Y_test = train_test_split(train_formatted_data)

# random forest regression model
model = ensemble.RandomForestRegressor()

# train the model
train(X_train, Y_train, model)
print("Training...")

# evaluate the model
print("Score: {}".format(evaluate(X_test, Y_test, model)))

# generate series over the prediction period
prediction_period = ["2018-06-22", "2018-06-23", "2018-06-24", "2018-06-25", "2018-06-26"]
location_ids=[168, 1403, 110]
vehicle_types=["13 Linja-autot", "12 KAIP", "11 HA-PA"]
generated = generate_prediction_series(model, dates=prediction_period, location_ids=location_ids, vehicle_types=vehicle_types)
generated_ts = to_ts_format(generated)
generated_ts.to_csv("prediction_22062018_26062018.csv", index=False)
print("Generated prediction data: prediction_22062018_26062018.csv.")



