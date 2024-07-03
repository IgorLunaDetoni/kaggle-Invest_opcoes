import yfinance as yf
import pandas as pd
import numpy as np
from prophet import Prophet
import datetime

def main():
    # Define the date range
    to_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    # Define the tickers
    tickers = ["VALE3.SA", "ITSA4.SA", "PETR4.SA"]

    # Download the data
    data = {ticker: yf.download(ticker, start="2024-01-01", end=to_date) for ticker in tickers}

    # Prepare the close prices DataFrame
    close_prices = pd.DataFrame({ticker: data[ticker]['Close'] for ticker in tickers})
    close_prices.fillna(method='ffill', inplace=True)
    close_prices.fillna(method='bfill', inplace=True)

    # Forecasting parameters
    forecast_period = 7

    # Initialize dictionaries to store models and forecasts
    models = {}
    forecasts = {}

    # Train the models and make forecasts
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

    # Prepare the data for Excel
    excel_data = {}
    for ticker in tickers:
        forecast_df = forecasts[ticker][['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'yhat_lower_std', 'yhat_upper_std', 'std']]
        forecast_df['type'] = 'prediction'
        actual_df = close_prices[[ticker]].reset_index()
        actual_df.columns = ['ds', 'y']
        actual_df['type'] = 'actual'
        combined_df = pd.concat([actual_df, forecast_df], ignore_index=True)
        excel_data[ticker] = combined_df

    # Save to Excel
    with pd.ExcelWriter('stock_forecasts_with_types.xlsx') as writer:
        for ticker in tickers:
            excel_data[ticker].to_excel(writer, sheet_name=ticker, index=False)

    print("Forecasts have been saved to stock_forecasts_with_types.xlsx")

if __name__ == "__main__":
    main()