# BCG Gamma Data Science Competition 2018
This project is a solution to BCG's data science competition in Summer 2018.

## About
The competition is based on Finnish Transport Agency's open road traffic data
(https://www.liikennevirasto.fi/web/en/open-data/). The data includes vehicle type specific traffic volumes 
at Automatic traffic measurement stations (TMS).

The assignment is to produce forecasting algorithm and a forecast of hourly
traffic volumes per vehicle category:
- Forecast period: 22.6.-26.6.2018
- Forecasts for three specified TMS locations: Askisto, Mäntsälä and Kemijärvi
- Solution submission DL: 21.6.2016

## Solution
All source code of the solution is included in Jupyter notebooks (.ipynb files):
- [1 Download Raw Data.ipynb](https://github.com/KovaVeikko/bcg-gamma/blob/master/1%20Download%20Raw%20Data.ipynb)
- [2 Refine Data.ipynb](https://github.com/KovaVeikko/bcg-gamma/blob/master/2%20Refine%20Data.ipynb)
- [3 Prediction.ipynb](https://github.com/KovaVeikko/bcg-gamma/blob/master/3%20Prediction.ipynb)
- [4 Visualization.ipynb](https://github.com/KovaVeikko/bcg-gamma/blob/master/4%20Visualization.ipynb)
- [5 User Interface.ipynb](https://github.com/KovaVeikko/bcg-gamma/blob/master/5%20User%20Interface.ipynb)

### Data
#### Historical TMS Data
Historical TMS data, or historical volumes, is provided in Excel workbooks: 
one workbook for each month and TMS station. The raw TMS data includes the following columns: 
- TMS station id 
- TMS Station name
- Date
- Direction (1 or 2)
- Vehicle type (7 different types)
- Volume for each hour 0-1, 1-2...

This data is available from 1/2010 to 5/2018.

#### Other Data Sources
It was encouraged by the competition organizers to apply additional data sources,
such as weather data. In fact, I did try to incorporate weather data from Finnish Meteorological 
Institute (http://ilmatieteenlaitos.fi/avoin-data-avattavat-aineistot) including 
daily rain and temperature statistics. However, it turned out that the weather data did
not improve the prediction performance, which is why I decided not to use it in the final solution.

### Methodology
#### Acquiring Data
First I had to decide what data to use for training. Obviously it would have been ideal to start with 
as much as possible historical data from all possible TMSs. However, as the data has been stored in
separate workbooks per each month and each location, I would have needed to download thousands of
Excel files. Thus, I decided to limit the training data to those three stations that I needed to
forecast volumes for: Askisto, Mäntsälä and Kemijärvi. To downloads these files, I wrote a script that
loops through each month from 2010 to 2017 and generates urls for the files.

Once the raw data was downloaded, I converted the xls files to csv format and combined them into a 
single csv file "raw_dataset.csv".

Finally, I improved the raw data by renaming the columns and adding calculated features
'week of year' and 'weekday'. 

#### Prediction Model
As the forecasting problem is a time series kind, i.e. having seasonality and trend components, 
a natural approach would be to use time series methods, such as ARMA or ARIMA. On the other hand,
in this era of deep learning, I considered trying Recurrent Neural Network (RNN) which would
be good at modelling complicated long-term relationships between the inputs.

However, before diving into the neural networks, I decided to try a more simple yet sophisticated approach: 
Random Forest Regression (RF). The motivation was that the underlying forecasting problem involves various
components that cause regular variations, such as public holidays, weekends, rush hours and seasons.
Specifically, as we are interested in period 22.6. - 26.6.2018 which happens to include the Midsummer's
Eve, we need to pay special attention to these variations. Furthermore, RF is significantly simpler
than RNN in terms of computing efficiency and hyper parameter tuning.

#### Testing

### Results

## Open Source Licences

