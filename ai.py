import httpx

# g4f import
try:
    from g4f.client import Client
    g4f_client = Client()
except:
    g4f_client = None

async def generate_ai_reply(user_id: int, message: str) -> str:
    prompt = f"You are a sweet Hindi speaking girlfriend. Talk romantically and funny. User said: {message}"

    # Try g4f first
    if g4f_client:
        try:
            response = g4f_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except:
            pass

    # Try phind AI
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                "https://phind-api.vercel.app/api/gpt",
                json={"prompt": prompt},
            )
            if resp.status_code == 200:
                return resp.json().get("text", "...")
    except:
        pass

    # If everything fails, return blank
    return "..."
