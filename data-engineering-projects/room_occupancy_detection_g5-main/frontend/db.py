from pymongo import MongoClient


class DatabaseConnectorHelper:
    def __init__(self, connection_url, db_name, col_name):
        self.client = MongoClient(connection_url)
        self.db = self.client[db_name]
        self.col = self.db[col_name]

    def get_latest_data(self) -> dict:
        query = self.col.find().limit(1).sort("_id", -1)
        result = list(query)
        if len(result):
            latest_record = result[0]
            # checking if all rooms data is available
            if len(latest_record.keys()) != 5:
                return {"message": f"data is not ready yet for {latest_record['_id']}"}
            else:
                return latest_record
        else:
            return {"message": "no data was found"}

    def get_paginated_records(self, per_page: int, page: int) -> dict:
        records_count = self.col.count_documents({})
        fetched_records = (
            self.col.find().sort("_id", -1).skip(per_page * (page - 1)).limit(per_page)
        )
        records = list(fetched_records)
        return {
            "total_records": records_count,
            "page": page,
            "showing": per_page,
            "records": records,
        }
