
from awd_min.celery import app
import time
@app.task
def celery_test_task():
    time.sleep(10) # simulation of any task that's going to take 10 secounds
    return "Tasl executed successfully."