import os

from base_logger import logger
from db import DatabaseConnectorHelper
from flask import Flask, flash, render_template, request

app_secret = os.environ.get("APP_SECRET")
connection_url = os.environ.get("MONGODB_CONNECTION_URL")
db_name = os.environ.get("MONGODB_DB_NAME")
col_name = os.environ.get("MONGODB_COL_NAME")

if None in (app_secret, connection_url, db_name, col_name):
    error_msg = "You need to specify APP_SECRET, MONGODB_CONNECTION_URL, MONGODB_DB_NAME and MONGODB_COL_NAME"
    logger.error(error_msg)
    raise Exception(error_msg)

app = Flask(__name__)
app.secret_key = app_secret

db_service = DatabaseConnectorHelper(connection_url, db_name, col_name)

# frontend end_points
@app.route("/")
def home():
    api_response = api_latest_data()
    if api_response.get("message"):
        flash(api_response["message"], "danger")
    return render_template("index.html", active_route="home", title="Home")


@app.route("/records")
def show_records():
    return render_template("records.html", active_route="records", title="Records")


# api end_points
@app.route("/api/latest_data")
def api_latest_data():
    latest_data = db_service.get_latest_data()
    return latest_data


@app.route("/api/records")
def api_records():
    page = request.args.get("page", default=1, type=int)
    per_page = 30
    records = db_service.get_paginated_records(per_page, page)
    return records


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
