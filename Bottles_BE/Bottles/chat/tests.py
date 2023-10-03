import requests

api_key = "VF.DM.xxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

user_id = "user_123"  # Unique ID used to track conversation state
user_input = "Hello world!"  # User's message to your Voiceflow project

body = {"action": {"type": "text", "payload": user_input}}

# Start a conversation
response = requests.post(
    f"https://general-runtime.voiceflow.com/state/user/{user_id}/interact",
    json=body,
    headers={
      "Authorization": 'VOICEFLOW_API_KEY',
      "versionID": "development"
    },
)

# Log the response
print(response.json())