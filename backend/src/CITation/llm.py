"""LLM client configuration.

All LLM calls go through ASU's CreateAI platform (https://docs.aiml.asu.edu/),
which exposes an OpenAI-compatible API, so we keep using the `openai` SDK and
just point it at CreateAI with a CreateAI project token.
"""

import os

from openai import OpenAI

TOKEN_ENV = "CREATEAI_SERVICE_TOKEN"
DEFAULT_BASE_URL = "https://api-main.aiml.asu.edu/v1"

# CreateAI model IDs are "provider/model_name" (e.g. "openai/gpt4o"), not
# OpenAI's names. `GET {base_url}/models` lists what your project can use.
MODEL = os.getenv("CREATEAI_MODEL", "openai/gpt4o")


def has_token() -> bool:
    return bool(os.getenv(TOKEN_ENV))


def make_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv(TOKEN_ENV),
        base_url=os.getenv("CREATEAI_BASE_URL", DEFAULT_BASE_URL),
    )
