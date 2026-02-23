import os
import httpx
import random
import time
from typing import Optional
from supabase import create_client, Client

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}

TIMEOUT = httpx.Timeout(connect=10.0, read=35.0, write=10.0, pool=10.0)

_client = httpx.Client(
    headers=DEFAULT_HEADERS,
    timeout=TIMEOUT,
    follow_redirects=True,
    http2=False,
)

def supabase_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)

def _sleep_polite(min_s: float = 1.2, max_s: float = 2.0) -> None:
    time.sleep(random.uniform(min_s, max_s))

def fetch_html(
    url: str,
    *,
    max_retries: int = 4,
    min_delay_s: float = 1.2,
    max_delay_s: float = 2.0,
    retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504),
) -> str:
    """
    Fetch HTML with:
      - session reuse
      - explicit timeouts
      - retry w/ exponential backoff + jitter
      - polite delay between attempts/successful calls
    """
    last_exc: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        # Delay *before* each attempt (prevents bursts in tight loops)
        _sleep_polite(min_delay_s, max_delay_s)

        try:
            resp = _client.get(url)

            if resp.status_code in retry_on_status:
                raise httpx.HTTPStatusError(
                    f"Retryable status {resp.status_code}",
                    request=resp.request,
                    response=resp,
                )

            resp.raise_for_status()
            return resp.text

        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.HTTPStatusError) as e:
            last_exc = e

            if attempt >= max_retries:
                raise

            # Exponential backoff with jitter (stronger than the base polite delay)
            backoff = (1.7 ** attempt) + random.uniform(0.3, 1.0)
            time.sleep(backoff)

    # Should never reach here
    raise last_exc if last_exc else RuntimeError("fetch_html failed")