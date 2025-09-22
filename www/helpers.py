import requests
import logging
import re

def validate_turnstile(secret, turnstile_response, remote_ip=None):
    data = {
        'secret': secret,
        'response': turnstile_response,
    }
    if remote_ip:
        data['remoteip'] = remote_ip

    try:
        response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        return result.get('success', False)
    except requests.exceptions.RequestException as e:
        logger = logging.getLogger(__name__)
        logger.error(f"validate_turnstile error: {e}")
        logger.error(data)
        return False

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None