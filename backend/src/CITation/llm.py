"""LLM client configuration.

All LLM calls go through ASU's CreateAI platform (https://docs.aiml.asu.edu/),
which exposes an OpenAI-compatible API, so we keep using the `openai` SDK and
just point it at CreateAI with a CreateAI project token.
"""

import os

from openai import OpenAI

from . import cache

TOKEN_ENV = "CREATEAI_SERVICE_TOKEN"
DEFAULT_BASE_URL = "https://api-main.aiml.asu.edu/v1"

# CreateAI model IDs are "provider/model_name" (e.g. "openai/gpt6_1_sol"), not
# OpenAI's names. `GET {base_url}/models` lists what your project can use.
MODEL = os.getenv("CREATEAI_MODEL", "openai/gpt6_1_sol")

# Request parameters that not every model accepts. CreateAI's /models listing
# says per model which of these it supports.
_OPTIONAL_PARAMS = ("temperature", "top_p", "max_tokens")

_model_info_cache: dict | None = None


def has_token() -> bool:
    return bool(os.getenv(TOKEN_ENV))


def make_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv(TOKEN_ENV),
        base_url=os.getenv("CREATEAI_BASE_URL", DEFAULT_BASE_URL),
    )


def _model_info(client: OpenAI, model: str) -> dict | None:
    """Return {supported, reasoning} for `model` from CreateAI's /models.

    Fetched once per process. Returns None if the listing is unavailable or
    doesn't include the model, in which case callers send params unchanged.
    """
    global _model_info_cache
    if _model_info_cache is None:
        _model_info_cache = {}
        try:
            for m in client.models.list():
                reasoning = getattr(m, "reasoning", None) or {}
                _model_info_cache[m.id] = {
                    "supported": set(getattr(m, "supported_parameters", None) or []),
                    "reasoning": bool(reasoning.get("default_enabled")),
                }
        except Exception as e:
            print(f"WARNING: could not fetch CreateAI model list: {e}")
            return None
        if model not in _model_info_cache:
            print(f"WARNING: model {model!r} is not in your CreateAI model list")
    return _model_info_cache.get(model)


def chat(client: OpenAI, **kwargs) -> str | None:
    """Run a chat completion with the configured model; return the reply text.

    Drops sampling params (temperature, top_p) the model doesn't accept, and
    drops `max_tokens` for models that reason by default, since reasoning
    tokens count against it and a small cap leaves an empty answer.

    Replies are cached (see cache.py), keyed on the exact request sent: model,
    messages and remaining params. A changed prompt or model is a miss. Empty
    replies and errors are not cached.
    """
    kwargs.setdefault("model", MODEL)
    info = _model_info(client, kwargs["model"])
    if info is not None:
        for param in _OPTIONAL_PARAMS:
            if param in kwargs and param not in info["supported"]:
                kwargs.pop(param)
        if info["reasoning"]:
            kwargs.pop("max_tokens", None)

    key = cache.make_key(kwargs)
    hit = cache.get("llm", key)
    if hit is not cache.MISSING:
        return hit
    response = client.chat.completions.create(**kwargs)
    text = response.choices[0].message.content
    if text and text.strip():
        cache.put("llm", key, text)
    return text
