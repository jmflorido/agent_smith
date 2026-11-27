# import requests
# import json
import os
from dotenv import load_dotenv
from dataclasses import dataclass, field
from openai import OpenAI, APIStatusError, RateLimitError
from icecream import ic
ic.configureOutput(includeContext=True, contextAbsPath=False)

"""
    Error Code 402 --> Credit limits
    Error Code 403 --> Budget limits
    Error Code 429 --ª Rate limits (free requests)

    Models OpenRouter
    Inkling (Thinking Machines)
    Nemotron 3 Ultra (NVIDIA)
    Gemma 4 (Google)

    ----------------------------------------------------------------------

    Models Groq (Openai format):
    Modelo  Peticiones/min	Peticiones/día	Tokens/min	Tokens/día
    openai/gpt-oss-120b	30	1.000	8.000	200.000
    openai/gpt-oss-20b	30	1.000	8.000	200.000
    qwen/qwen3.8-27b	30	1.000	8.000	200.000

    [] OpenAI SDK
    [] Excepciones RateLimitError y APIStatusError
    
"""

load_dotenv()

@dataclass(frozen=True)
class LLMProvider:
    sdk: str
    provider: str
    base_url: str
    api_key: str
    model: str
    extra_body: dict = field(default_factory=dict)

PROVIDERS = [
    LLMProvider(
        sdk="openai",
        provider="openrouter",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        extra_body={"reasoning": {"enabled": False}}
        ),
    LLMProvider(
        sdk="openai",
        provider="google",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini-4-hydrogen",
        extra_body={"reasoning_effort": "low"}
        ),
    LLMProvider(
        sdk="openai",
        provider="google",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini-3.5-flash-lite",
        extra_body={"reasoning_effort": "low"}
        ),
    LLMProvider(
        sdk="openai",
        provider="groq",
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-120b",
        extra_body={"reasoning_effort": "low"}
        ),
        # LLMProvider(
        #     sdk="openai",
        #     provider="openrouter",
        #     base_url="https://openrouter.ai/api/v1",
        #     api_key=os.getenv("OPENROUTER_API_KEY"),
        #     model="google/gemma-4-26b-a4b-it:free",
        #     extra_body={"reasoning": {"enabled": False}}
        # ),

        # LLMProvider(
        #     sdk="openai",
        #     provider="openrouter",
        #     base_url="https://openrouter.ai/api/v1",
        #     api_key=os.getenv("OPENROUTER_API_KEY"),
        #     model="nvidia/nemotron-3.5-super-vl:free",
        #     extra_body={"reasoning": {"enabled": False}}
        # ),
]


# def get_answer(input_msg: str) -> None:
#     response = requests.post(
#         url="https://openrouter.ai/api/v1/responses",
#         headers={
#             "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#             # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#             # "X-OpenRouter-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#         },
#         json={
#             # "model": "~openai/gpt-sol-latest",
#             "model": "nvidia/nemotron-3.5-super-vl:free",
#             # "input": "What is the meaning of life?",
#             "input": input_msg,
#             "reasoning": {"enabled": False}
#             }
#         )

#     print(json.dumps(response.json(), indent=2))

def get_answer(input_msg: str) -> None:
    for llm in PROVIDERS:
        if not llm.api_key:
            continue
        try:
            print(f"Using model: {llm.model} from {llm.provider} provider.")
            client = OpenAI(
                api_key=llm.api_key,
                base_url=llm.base_url,
                timeout=30,
            )
            response = client.chat.completions.create(
                model=llm.model,
                messages=[
                    {"role": "developer", "content": "Talk like a pirate."},
                    {"role": "user", "content": input_msg}],
                # max_tokens=250,
                extra_body=llm.extra_body,
            )
            if response:
                return response
        except (RateLimitError, APIStatusError) as e:
            print(f"[{llm.provider}] {e.status_code}: {e.message}. Trying next provider...")
            continue
    return ""


# def get_openrouter_spent() -> None:
#     response = requests.get(
#         url="https://openrouter.ai/api/v1/key",
#         headers={
#             "Authorization": f"Bearer {OPENROUTER_API_KEY}"
#         }
#     )

#     print(json.dumps(response.json(), indent=2))

    
response = get_answer(input_msg="What is a RAG?")
# ic(response)
ic(response.choices[0].message.content)
# print("===" * 30)
# print("\n\n")
# get_openrouter_spent()

