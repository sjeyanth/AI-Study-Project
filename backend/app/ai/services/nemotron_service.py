from openai import OpenAI

from app.settings import NVIDIA_API_KEY


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY,
)


def ask_nemotron(message: str) -> str:

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI productivity assistant. "
                    "Help users with studying, planning, notes, "
                    "goals, budgeting and productivity."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        temperature=0.3,
        max_tokens=50,
    )

    return response.choices[0].message.content


def ask_nemotron_simple(
    prompt: str
) -> str:

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.3,
        max_tokens=200,
    )

    return response.choices[0].message.content