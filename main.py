from phase1 import encode_image, analyze_image_with_query, query, model

image_path = "test.jpg"

encoded_image = encode_image(image_path)

print("Encoding image and sending to Groq...")

response = analyze_image_with_query(query, model, encoded_image)

print(response)