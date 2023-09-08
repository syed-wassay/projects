import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from service import ExtractorService

extractor = ExtractorService()

# initialize scheduler
scheduler = BlockingScheduler()

# run every minute
scheduler.add_job(
    extractor.get_luxmeter_data,
    "cron",
    second="0",
    next_run_time=(datetime.datetime.now()),
)

# start scheduler
scheduler.start()
