from celery import group
from utils.celery.celery_config import celery_app
from utils.celery.health_check.perform_health_check import perform_health_check
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from celery.schedules import schedule



if __name__ == "__main__":
    # Example: List of 10,000 unique URLs
    urls = [
        "https://www.google.com",
        "https://timesofindia.com",
        "https://www.yahoo.com",
        "https://www.cnn.com",
        "https://www.foxnews.com",
        "https://www.thehindu.com",
        "https://www.vzw.com",
        "https://www.verizon.com",
        "https://www.att.com",
        "https://www.greatandhra.com",
        "https://www.youtube.com",
        "https://www.nfl.com",
        "https://www.nba.com",
        "https://www.pgatour.com",
        # Add more unique host URLs here
    ]

    # Divide URLs into manageable batches (optional for scalability)
    # while True:
    #     batch_size = 50
    #     url_batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]
    #
    #     # Schedule health checks for each batch
    #     task_group = group(perform_health_check.s(batch, concurrency_limit=50) for batch in url_batches)
    #     result = task_group.apply_async()
    #
    #     print(f"Scheduled {len(url_batches)} batches for health checks. Task Group ID: {result.id}")
    #     try:
    #         http_data=result.get(timeout=7)
    #         logger.info(f"{http_data}")
    #     except Exception as err:
    #         logger.error(f"error in {err}")
    #     finally:
    #         pass

