from flask import current_app

from app.integrations.http_client import NotifyHTTPClient

def get_notify_client() -> NotifyHTTPClient:
    return NotifyHTTPClient()

def get_max_retries() -> int:
    return current_app.config["MAX_RETRIES"]