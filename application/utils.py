from flask import request, url_for
from urllib.parse import urlparse, urljoin


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_next_url():
    next = request.args.get('next')
    if not is_safe_url(next) or not next:
        return url_for('index')
    return next