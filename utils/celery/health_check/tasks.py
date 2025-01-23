import httpx
import aiohttp
import asyncio
from utils.celery.celery_config import celery_app
from celery.schedules import crontab
from celery import shared_task,Task
import logging
from datetime import datetime
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
# Configure logging
from logpkg.log_kcld import LogKCld, log_to_file

logger = LogKCld()
# urls = [
#     "https://www.google.com",
#     "https://timesofindia.com",
#     "https://www.yahoo.com",
#     "https://www.cnn.com",
#     "https://www.foxnews.com",
#     "https://www.thehindu.com",
#     "https://www.vzw.com",
#     "https://www.verizon.com",
#     "https://www.att.com",
#     "https://www.greatandhra.com",
#     "https://www.youtube.com",
#     "https://www.nfl.com",
#     "https://www.nba.com",
#     "https://www.pgatour.com",
#     # Add more unique host URLs here
# ]
#
# celery_app.conf.beat_schedule = {
#     'run-health-checks-every-5-seconds': {
#         'task': 'utils.celery.health_check_tasks.perform_health_check',
#         'schedule': 5.0,
#         'args': urls
#     },
# }

class AsyncTask(Task):
    def __call__(self, *args, **kwargs):
        # Run the asyncio loop within the Celery task
        return asyncio.run(self.run(*args, **kwargs))


# List of URLs to check

@celery_app.task
@shared_task(bind=True)
@log_to_file(logger)
def perform_health_check(self, urls, concurrency_limit=30):
    """
    Perform health checks for a given list of URLs with concurrency control.
    """

    async def check_url(url):
        try:
            ct = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            async with httpx.AsyncClient(timeout=5) as client:
                logger.info(f"Checking: {url}")
                response = await client.get(url)
                return {'current time': ct, 'url': url, 'status': 'healthy' if response.status_code == 200 else 'unhealthy', 'status_code': response.status_code}
        except httpx.RequestError as exc:
            logger.error(f"Failed: {url} -> {exc}")
            return {'url': url, 'status': 'unhealthy', 'status_code': None, 'error': str(exc)}

    async def schedule_checks(urls, concurrency_limit):
        semaphore = asyncio.Semaphore(concurrency_limit)

        async def limited_check(url):
            async with semaphore:
                return await check_url(url)

        # Schedule checks for the provided URLs
        results = [await limited_check(url) for url in urls]
        return results

    # Use asyncio.run to execute the coroutine
    return asyncio.run(schedule_checks(urls, concurrency_limit))


@celery_app.task
@shared_task(bind=True)
@log_to_file(logger)
def perform_http_check(urls):
    results = []

    def health_check(url):
        try:
            ct = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"Checking: {url}")
            response = requests.get(url, timeout=5)
            return {'current time': ct, 'url': url, 'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'status_code': response.status_code}
        except requests.RequestException as exc:
            logger.error(f"Failed: {url} -> {exc}")
            return {'url': url, 'status': 'unhealthy', 'status_code': None, 'error': str(exc)}

    # Perform health checks with threading
    with ThreadPoolExecutor(max_workers=50) as executor:
        print(f"Urls for check are {urls}")
        futures = {executor.submit(health_check, url): url for url in urls}
        for future in as_completed(futures):
            results.append(future.result())
    return results


# Function to perform a health check



@celery_app.task(base=AsyncTask)
@log_to_file(logger)
async def health_check_task(urls, max_concurrency=100):
    async def health_check(url, session):
        try:
            ct = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"Checking: {url}")
            async with session.get(url, timeout=5,allow_redirects=False,verify_ssl=False) as response:
                print(str(response.status))
                if response.status == 200:
                    status='healthy'
                else:
                    status='unhealthy'
                logger.info(f"current time: {ct}, url: {url}, status: {status},status_code: {response.status}")
                return {'current time': ct, 'url': url, 'status': 'healthy' if response.status == 200 else 'unhealthy',
                    'status_code': response.status}
        except Exception as exc:
            logger.info(f"current time: {ct}, url: {url}, status: 600,status_code: unhealthy error: {str(exc)}")
            return {'url': url, 'status': 'unhealthy', 'status_code': None, 'error': str(exc)}

    async def health_check_limited(url, session, semaphore):
        async with semaphore:
            return await health_check(url, session)

    async def check_all_urls():
        semaphore = asyncio.Semaphore(max_concurrency)
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = [health_check_limited(url, session, semaphore) for url in urls]
            for task in asyncio.as_completed(tasks):
                results.append(await task)
        return results

    # Run the async function with concurrency control
    return await check_all_urls()










