import requests

# AI Proxy API Key
API_KEY = "your_ai_proxy_token"

# Read email content from file
with open("/data/email.txt", "r", encoding="utf-8") as file:
    email_content = file.read()

# Send the email content to GPT-4 for extraction
response = requests.post(
    "https://api.aiproxy.io/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Extract the sender's email address from the provided email content and return only the email address."},
            {"role": "user", "content": email_content}
        ]
    }
)

# Extract the email from the response
email_address = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()

# Save only the email address to a file
with open("/data/email-sender.txt", "w") as output_file:
    output_file.write(email_address)

print("Sender's email address extracted and saved successfully!")
