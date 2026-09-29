import json
import os
import urllib.error
import urllib.request


def load_env():
  if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
      for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
          key, value = line.split("=", 1)
          os.environ[key.strip()] = value.strip().strip('"').strip("'")


def main():
  load_env()

  api_key = os.getenv("MY_SECRET")

  if not api_key:
    raise ValueError("MY_SECRET missing in .env file!")

  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

  print("=" * 50)
  print("🤖 Connected to Gemini API successfully!")
  print("Type your message and press Enter (or type 'exit' to quit):")
  print("=" * 50)

  while True:
    user_input = input("\nYou: ")

    if user_input.strip().lower() in ["exit", "quit"]:
      print("\n👋 Conversation closed. Goodbye!")
      break

    if not user_input.strip():
      continue

    payload = {"contents": [{"parts": [{"text": user_input}]}]}

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    req = urllib.request.Request(url, data=data, headers=headers)

    try:
      with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        bot_response = result["candidates"][0]["content"]["parts"][0]["text"]
        print(f"\nGemini:\n{bot_response}")

    except urllib.error.HTTPError as e:
      print(f"\nHTTP Error: {e.code} - {e.reason}")
    except Exception as e:
      print(f"\nError: {e}")


if __name__ == "__main__":
  main()
bot_response = result["candidates"][0]["content"]["parts"][0]["text"]