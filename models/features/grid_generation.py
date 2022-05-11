import pandas as pd
from datetime import datetime

if __name__ == "__main__":
    print(" running code ... ")
    # import and process data
    crime_df = pd.read_csv('../../data/interventionscitoyendo.csv', sep=',', encoding='latin-1')
    crime_data = crime_df[crime_df['LATITUDE'] != 0]
    date_data = [datetime.strptime(crime_data.iloc[i]['DATE'], '%Y-%m-%d') for i in range(len(crime_data))]
    crime_year = [date_data[i].year for i in range(len(date_data))]
    crime_month = [date_data[i].month for i in range(len(date_data))]
    crime_data = crime_data.assign(CRIME_YEAR=crime_year)
    crime_data = crime_data.assign(CRIME_MONTH=crime_month)

    # find extrema
    extrema = (crime_data['LONGITUDE'].min(), crime_data['LATITUDE'].min())
    minima = (crime_data['LONGITUDE'].max(), crime_data['LATITUDE'].max())
    print('extrema', extrema)
    print('minima', minima)

    # build grid
