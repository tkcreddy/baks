from celery_config import app

# Start the worker
if __name__ == "__main__":
    app.worker_main()
