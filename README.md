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
#### Downloading and Cleaning Data

#### Prediction Model

### Testing

### Results

## Licences

