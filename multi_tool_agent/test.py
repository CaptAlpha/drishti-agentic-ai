import requests
import json

url = "https://adk-default-service-name-450141277196.us-central1.run.app/run_sse"

payload = json.dumps({
  "app_name": "multi_tool_agent",
  "user_id": "user_123",
  "session_id": "session_abc",
  "new_message": {
    "role": "user",
    "parts": [
      {
        "text": "how is the weather in new york"
      }
    ]
  },
  "streaming": False
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
