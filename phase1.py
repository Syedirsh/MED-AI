# Step 1: Setup GROQ API Key
import os
import base64
from groq import Groq

# Load API Key from Environment Variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Step 2: Convert Image to Base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Step 3: Setup Multimodal LLM
query = "Is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"


def analyze_image_with_query(query, model, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    },
                },
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return chat_completion.choices[0].message.content


# ==========================

if __name__ == "__main__":
    image_path = "test.jpg"

    if not os.path.exists(image_path):
        print(f"Error: '{image_path}' not found.")
    elif not GROQ_API_KEY:
        print("Error: GROQ_API_KEY not found in environment variables.")
    else:
        encoded = encode_image(image_path)
        result = analyze_image_with_query(query, model, encoded)

        print("\nAI Response:\n")
        print(result)