import sys
import os

PROJECT_DIR = (
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\api_watchbot"
)
sys.path.append(PROJECT_DIR)

import watchbot as wb


def test_api_list():
    assert wb.API_LIST is not None
    assert type(wb.API_LIST) is list


def test_telegram_token():
    assert wb.TELEGRAM_TOKEN is not None
    assert type(wb.TELEGRAM_TOKEN) is str


def test_telegram_group_id():
    assert wb.TELEGRAM_GROUP_ID is not None
    assert type(wb.TELEGRAM_GROUP_ID) is str


def test_check_api_status():
    api = {"name": "test", "url": "https://httpstat.us/200"}
    status_code, status_text = wb.check_api_status(api)
    assert status_code == 200
    assert status_text == "OK"


def test_check_api_status_timeout():
    api = {"name": "test", "url": "https://httpstat.us/200?sleep=15000"}
    status_code, status_text = wb.check_api_status(api)
    assert status_code == 408
    assert status_text == "Request timed out!"


def test_check_api_status_error_404():
    api = {"name": "test", "url": "https://httpstat.us/404"}
    status_code, status_text = wb.check_api_status(api)
    assert status_code == 404
    assert status_text == "404 Not Found"


def test_check_api_status_error_500():
    api = {"name": "test", "url": "https://httpstat.us/500"}
    status_code, status_text = wb.check_api_status(api)
    assert status_code == 500
    assert status_text == "500 Internal Server Error"


def test_check_api_status_error_503():
    api = {"name": "test", "url": "https://httpstat.us/503"}
    status_code, status_text = wb.check_api_status(api)
    assert status_code == 503
    assert status_text == "503 Service Unavailable"


def test_check_api_status_error_504():
    api = {"name": "test", "url": "https://httpstat.us/504"}
    status_code, status_text = wb.check_api_status(api)
    assert status_code == 504
    assert status_text == "504 Gateway Timeout"
