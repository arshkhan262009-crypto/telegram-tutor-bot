import os
import telebot
from google import genai
from PIL import Image

# Fetch tokens securely from the cloud environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

system_instruction = "You are an elite, empathetic, and human-like academic tutor. Answer students questions step-by-step with an encouraging tone. Always structure complex"

@bot.message_handler(content_types=['text', 'photo'])
def handle_student_messages(message):
    try:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            with open("temp.jpg", "wb") as f:
                f.write(downloaded_file)
                
            img = Image.open("temp.jpg")
            caption = message.caption if message.caption else "Please solve and explain this step-by-step."
            
            response = model.generate_content([caption, img])
            bot.reply_to(message, response.text)
            os.remove("temp.jpg")
            
        elif message.content_type == 'text':
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
            
    except Exception as e:
        print(f"Error encountered: {e}")

if name == "main":
    print("Your Student Tutor Bot is running securely...")
    bot.infinity_polling()
