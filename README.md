# Meraki Data analysis through confidence interval

In this code we analyze data from Meraki API. We are going to use Bollinger Bands analysis for Meraki data an provide a confidence inteval to detect data that goes beyond 2 standard deviation

##Installation
Install `docker` and `docker-compose` previously.

Clone the repo
```bash
git clone https://github.com/mighidalgo/ikusi-devnet.git`
```

Go to your project folder
```bash
cd ikusi-devnet`
```

Run docker compose
```bash
docker-compose up -d`
```

Now you have the project up and running, enter the URL
```bash
http://localhost:8001/fetch`
```

## Configuration

- In order to fetch data from Meraki API, we need to set this env variables in the `docker-compose` file
  - `BASE_URL` - Required, Meraki API URL.
  - `API_KEY` - Required, Apikey to access the API.
  - `ORG_ID` - Optional, if you want the data from a specific organization of the Meraki data, set this var.
