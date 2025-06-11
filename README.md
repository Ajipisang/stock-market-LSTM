
# README

This project is part of my homework assignment. Creating a Python-based stock price prediction tool using the ARIMA time series model.


## module Installation

module Installation

```bash
  pip install requests
```
```bash
  pip install python-dotenv
```
## .ENV

need env file 

```bash
  API_KEY=your_alpha_vantage_api_key
  FOLDER=your_output_folder_path (copy data_csv absolute path)
```


## API Reference

#### url : https://www.alphavantage.co/


#### Get company symbol

```http
  GET /query?function=SYMBOL_SEARCH&keywords={queryName}&apikey={api_key}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `queryName` | `string` | **Required**.  query |
| `api_key` | `string` | **Required**.  API key |


#### Get stock market price

```http
  GET /query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `symbol`      | `string` | **Required**. company symbol |
| `api_key` | `string` | **Required**.  API key |




