import sys
import logging
import google.generativeai as genai
import config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

def test():
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Merhaba, bu bir test mesajıdır.")
        print("Response (Flash):", response.text)
    except Exception as e:
        print("Exception (Flash):", e)

if __name__ == "__main__":
    test()
