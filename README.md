# Meraki Data analysis through confidence interval

In this code we analyze data from Meraki API. We are going to use Bollinger Bands analysis for Meraki data an provide a confidence inteval to detect data that goes beyond 2 standard deviation.
We've enhanced our Meraki data analysis toolkit by integrating the Isolation Forest algorithm. This powerful method is excellent for detecting anomalies in large datasets, helping to identify unusual patterns or outliers that standard analysis might miss.

Algorithms:
- Bollinger Bands
- Isolation Forest

## Installation
Install `docker` and `docker-compose` previously.

Clone the repo
```bash
git clone https://github.com/mighidalgo/ikusi-devnet.git
```

Go to your project folder
```bash
cd ikusi-devnet
```

## Usage

Run docker compose
```bash
docker-compose up -d
```

Now you have the project up and running, enter the URL
```bash
http://localhost:8001/bollinger-bands - Bollinger Bands algorithm
http://localhost:8001/isolation-forest - Isolation forest algorithm
```

## Configuration

- In order to fetch data from Meraki API, we need to set this env variables in the `docker-compose` file
  - `BASE_URL` - Required, Meraki API URL.
  - `API_KEY` - Required, Apikey to access the API.
  - `ORG_ID` - Optional, if you want the data from a specific organization of the Meraki data, set this var.
  - `ISOLATION_SENSITIVITY` - Required, value used with the isolation forest algorithm

## Example
- Run the Isolation Forest analysis on your Meraki dataset to identify potential anomalies. The output will list any data points that are considered statistically unusual, aiding in deeper data investigations.
- Our tool now includes an analysis feature using Bollinger Bands, a popular tool in financial data analysis. Bollinger Bands are a type of statistical chart characterizing the prices and volatility of a financial instrument or commodity over time. This method is particularly useful in identifying the high and low prices of an asset relative to its previous trades.

## Additional Notes
The Isolation Forest algorithm is particularly effective on large datasets. Performance may vary depending on the size and complexity of your data.

## Hardware and Software requirements

You can run this project by just installing `docker` and `docker-compose` on your machine or server.
Recommendend hardware is 4 GB of ram and a dual core processor.
