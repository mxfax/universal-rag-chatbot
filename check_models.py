import google.generativeai as genai

genai.configure(api_key="AIzaSyDV1kwK0KcBOnInOpdOwutuSAuqMgLq82E")

print("Listing available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)