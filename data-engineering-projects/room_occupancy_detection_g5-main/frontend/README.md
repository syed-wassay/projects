## frontend

### Purpose
This service was created to display predicted data in real-time. The service uses `flask` to expose `api endpoints` which later on are being consumed by making `ajax` calls from the browser. 

### Requirements
The service requires following `ENV VARIABLES`

`APP_SECRET` (kafka hostname/ip with port)

`MONGODB_CONNECTION_URL` (connection uri/url of the mongodb database)

`MONGODB_DB_NAME` (name of database to read data from)

`MONGODB_COL_NAME` (name of collection to fetch data from)

### API Reference

#### Get latest record

```http
  GET /api/latest_data
```

#### Get paginated records

```http
  GET /api/records?page=PAGE_NO
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `page` | `int` | **Default**. 1 |


### Running the service
You can use `python3` or `docker` to run the service. You will find `requirements.txt` and a `Dockerfile` as well inside the service directory
