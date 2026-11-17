"""Persistent cache for results from external services.

Everything the pipeline gets from outside the process is plain text: GROBID's
TEI XML, Semantic Scholar / OpenAlex JSON, LLM completions, and PDF→markdown
output. It's cheap to store and expensive to recompute (network round trips,
rate-limit sleeps, GROBID's up-to-120 s calls, billed LLM tokens), so it all
goes through this module.

Only *raw* responses are cached, keyed by the exact request (PDF bytes are
hashed, API keys are left out of the key). Parsing and anomaly detection
always re-run, so code fixes apply to cached papers too, and a changed prompt,
model or request parameter is automatically a cache miss.

Storage is a single SQLite file (WAL mode, one connection per thread). Cache
errors are logged and treated as misses: the cache never breaks the pipeline.

Environment:
    CITADEL_CACHE=0            disable reading and writing the cache
    CITADEL_CACHE_DIR=path     where cache.sqlite3 lives (default: <repo>/.cache/citadel)
    CITADEL_CACHE_TTL_DAYS=30  max age for Semantic Scholar / OpenAlex entries
"""

import hashlib
import json
import os
import sqlite3
import threading
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

import requests

ENABLED = os.getenv("CITADEL_CACHE", "1").strip().lower() not in ("0", "false", "no", "off")
CACHE_DIR = Path(
    os.getenv("CITADEL_CACHE_DIR")
    or Path(__file__).resolve().parents[3] / ".cache" / "citadel"
)
# Scholarly metadata (citation counts, new ORCIDs, ...) drifts, so API entries
# expire. GROBID, markdown and LLM entries are pure functions of their inputs.
API_TTL = float(os.getenv("CITADEL_CACHE_TTL_DAYS", "30")) * 86400

MISSING = object()  # get() result for a miss; distinct from a cached None

_local = threading.local()
_stats_lock = threading.Lock()
_hits: Counter = Counter()
_misses: Counter = Counter()

_throttle_lock = threading.Lock()
_last_request_end: dict[str, float] = {}


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


def _conn() -> sqlite3.Connection:
    path = CACHE_DIR / "cache.sqlite3"
    cached = getattr(_local, "conn", None)
    if cached is not None and cached[0] == path:
        return cached[1]
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cache ("
        " ns TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL,"
        " created REAL NOT NULL, PRIMARY KEY (ns, key))"
    )
    _local.conn = (path, conn)
    return conn


def _json_default(obj):
    if isinstance(obj, (bytes, bytearray, memoryview)):
        return {"sha256": hashlib.sha256(bytes(obj)).hexdigest()}
    if isinstance(obj, (set, frozenset)):
        return sorted(obj)
    raise TypeError(f"cache key part not serializable: {type(obj).__name__}")


def make_key(*parts) -> str:
    """Stable hash of JSON-able parts. Bytes (e.g. a PDF) are hashed by content."""
    blob = json.dumps(parts, sort_keys=True, separators=(",", ":"), default=_json_default)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def get(ns: str, key: str, max_age: float | None = None):
    """Return the cached value, or MISSING."""
    if not ENABLED:
        return MISSING
    try:
        row = _conn().execute(
            "SELECT value, created FROM cache WHERE ns = ? AND key = ?", (ns, key)
        ).fetchone()
    except sqlite3.Error as e:
        print(f"WARNING: cache read failed ({ns}): {e}")
        row = None
    if row is not None and (max_age is None or time.time() - row[1] <= max_age):
        with _stats_lock:
            _hits[ns] += 1
        return json.loads(row[0])
    with _stats_lock:
        _misses[ns] += 1
    return MISSING


def put(ns: str, key: str, value) -> None:
    if not ENABLED:
        return
    try:
        conn = _conn()
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (ns, key, value, created) VALUES (?, ?, ?, ?)",
                (ns, key, json.dumps(value), time.time()),
            )
    except (sqlite3.Error, TypeError, ValueError) as e:
        print(f"WARNING: cache write failed ({ns}): {e}")


def clear(ns: str | None = None) -> int:
    """Delete cached entries (all, or one namespace). Returns rows deleted."""
    conn = _conn()
    with conn:
        if ns is None:
            n = conn.execute("DELETE FROM cache").rowcount
        else:
            n = conn.execute("DELETE FROM cache WHERE ns = ?", (ns,)).rowcount
    conn.execute("VACUUM")
    return n


def stats() -> dict:
    """Hit/miss counts per namespace since the last reset_stats()."""
    with _stats_lock:
        namespaces = sorted(set(_hits) | set(_misses))
        return {ns: {"hits": _hits[ns], "misses": _misses[ns]} for ns in namespaces}


def reset_stats() -> None:
    with _stats_lock:
        _hits.clear()
        _misses.clear()


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


@dataclass
class Response:
    """The subset of requests.Response the pipeline uses, cacheable as JSON."""

    status_code: int
    text: str
    headers: dict = field(default_factory=dict)

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}: {self.text[:200]}")


def _throttle(url: str, min_interval: float) -> None:
    """Wait until `min_interval` s have passed since the last request to this host."""
    host = urlsplit(url).netloc
    with _throttle_lock:
        wait = _last_request_end.get(host, 0.0) + min_interval - time.monotonic()
    if wait > 0:
        time.sleep(wait)


def request(
    ns: str | None,
    method: str,
    url: str,
    *,
    params=None,
    data=None,
    json_body=None,
    files=None,
    headers=None,
    timeout: float = 30,
    max_age: float | None = None,
    cache_statuses: tuple[int, ...] = (200,),
    min_interval: float = 0.0,
) -> Response:
    """HTTP request whose response is cached under namespace `ns`.

    Only responses with a status in `cache_statuses` are stored, so transient
    failures (429, 5xx, timeouts) are always retried. `headers` are not part of
    the key, so API keys never reach the cache. `ns=None` skips the cache but
    still applies `min_interval`, the per-host rate limit, which only applies
    to real network calls: cache hits return immediately.

    Network errors propagate as requests exceptions, as with requests itself.
    """
    key = None
    if ns is not None:
        file_parts = {name: spec[1] for name, spec in (files or {}).items()}
        key = make_key(method.upper(), url, params, data, json_body, file_parts)
        hit = get(ns, key, max_age)
        if hit is not MISSING:
            return Response(hit["status"], hit["text"], hit.get("headers", {}))

    if min_interval:
        _throttle(url, min_interval)
    try:
        r = requests.request(
            method,
            url,
            params=params,
            data=data,
            json=json_body,
            files=files,
            headers=headers,
            timeout=timeout,
        )
    finally:
        if min_interval:
            with _throttle_lock:
                _last_request_end[urlsplit(url).netloc] = time.monotonic()

    content_type = r.headers.get("content-type")
    resp = Response(
        r.status_code, r.text, {"content-type": content_type} if content_type else {}
    )
    if key is not None and r.status_code in cache_statuses:
        put(ns, key, {"status": resp.status_code, "text": resp.text, "headers": resp.headers})
    return resp
