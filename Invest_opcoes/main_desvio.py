import yfinance as yf
import pandas as pd
import numpy as np
from prophet import Prophet
import datetime
import plotly



def main():
    # Define the date range
    to_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    # Define the tickers
    tickers = ["VALE3.SA", "ITSA4.SA", "PETR4.SA"]
    data = {ticker: yf.download(ticker, start="2024-01-01", end=to_date) for ticker in tickers}
    close_prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in tickers})
    forecast_period = 7

    models = {}
    forecasts = {}

    for ticker in tickers:
        df = close_prices[[ticker]].reset_index()
        df.columns = ['ds', 'y']
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=forecast_period)
        forecast = model.predict(future)
        std_dev = close_prices[ticker].rolling(window=22).std().iloc[-1] * 2
        forecast['std'] = std_dev
        forecast['yhat_upper_std'] = forecast['yhat'] + forecast['std']
        forecast['yhat_lower_std'] = forecast['yhat'] - forecast['std']
        models[ticker] = model
        forecasts[ticker] = forecast

    excel_data = {}
    for ticker in tickers:
        forecast_df = forecasts[ticker][['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'yhat_lower_std', 'yhat_upper_std', 'std']]
        forecast_df['type'] = 'prediction'
        actual_df = close_prices[[ticker]].reset_index()
        actual_df.columns = ['ds', 'y']
        actual_df['type'] = 'actual'
        combined_df = pd.concat([actual_df, forecast_df], ignore_index=True)
        excel_data[ticker] = combined_df

    with pd.ExcelWriter('stock_forecasts_with_types.xlsx') as writer:
        for ticker in tickers:
            excel_data[ticker].to_excel(writer, sheet_name=ticker, index=False)

    print("Forecasts have been saved to stock_forecasts_with_types.xlsx")

def excel_sheets_to_csvs(file_path):
    # Read the Excel file
    excel_data = pd.ExcelFile(file_path)
    csv_list = []

    for sheet_name in excel_data.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        csv_file_path = f"{sheet_name}.csv"
        df.to_csv(csv_file_path, index=False)
        csv_list.append(csv_file_path)
    
    return csv_list

if __name__ == "__main__":
    main()
    
    # Path to your Excel file
    file_path = 'stock_forecasts_with_types.xlsx'

    # Convert and save the CSVs in a list
    csv_files = excel_sheets_to_csvs(file_path)

    # Print the list of CSV file paths
    print(csv_files)