import os

for k, v in os.environ.items():
    if any(x in k.upper() for x in ["BASE_URL", "GEMINI", "NEW_API", "API_KEY"]):
        if len(v) > 20:
            v_masked = v[:6] + "..." + v[-4:]
        else:
            v_masked = v
        print(f"ENV: {k} = {v_masked}")
