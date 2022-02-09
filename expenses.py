import datetime
import pytz
import re


def add_expense(message):
    data = _parse_message(message)
    return data


def _parse_message(raw_message: str):
    """Parcing new message"""
    regexp_result = re.match(r"([\d ]+,[\d]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise Exception(
            "Not correct message, add message like example, "
            "example:\n15,13 or 10,00 resto")
    amount = regexp_result.group(1).replace(" ", "")
    comment = regexp_result.group(2).strip().lower()
    data = [[date(), comment, amount]]
    return data


def _get_now_formatted() -> str:
    """Return time formated"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Return date and time timezone Europe Paris"""
    tz = pytz.timezone("Europe/Paris")
    now = datetime.datetime.now(tz)
    return now


def date():
    return _get_now_formatted()
