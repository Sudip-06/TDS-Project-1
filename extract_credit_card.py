import requests

# AI Proxy API Key
API_KEY = "your_ai_proxy_token"

# Load the image
image_path = "/data/credit_card.png"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# Send the image to GPT-4 Vision
response = requests.post(
    "https://api.aiproxy.io/v1/images/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    files={"file": image_data},
    json={"instructions": "Extract and return only the credit card number without spaces."}
)

# Extract the card number from the response
card_number = response.json().get("text", "").replace(" ", "")

# Save to file
with open("/data/credit-card.txt", "w") as output_file:
    output_file.write(card_number)

print("Credit card number extracted and saved successfully!")
