import pandas as pd
crime_df = pd.read_csv('../data/interventionscitoyendo.csv', sep=',', encoding='latin-1')

print(crime_df.head())
