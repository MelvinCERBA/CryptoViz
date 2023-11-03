# docs: https://faust.readthedocs.io/en/latest/
# By Celery dev (handle kafka)
import faust
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
import chromedriver_autoinstaller

from tasks import scraper1, scraper2

load_dotenv()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

# Define the Faust app with Kafka broker URL
app = faust.App('crypto_scrape_app', broker='kafka://' + os.getenv('KAFKA_BROKER'))
executor = ThreadPoolExecutor()

@app.on_worker_init
async def setup_executor(app, **kwargs):
    global executor
    executor = ThreadPoolExecutor()

@app.timer(interval=30)
async def scrape_task1():
    await app.loop.run_in_executor(executor, scraper1.scrape)

@app.timer(interval=30)
async def scrape_task2():
    await app.loop.run_in_executor(executor, scraper2.scrape)

# Run the Faust worker
# if __name__ == '__main__':
#     app.main()

# CMD ["faust", "-A", "main", "worker", "-l", "info"]