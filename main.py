import os
import telebot
from PIL import Image
from google import genai

# Fetching tokens from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

system_instruction = "You are an elite, empathetic, and human-like academic tutor. Answer students questions step-by-step with an encouraging tone. Always structure complex answers clearly."

@bot.message_handler(content_types=['text', 'photo'])
def handle_student_messages(message):
    try:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            with open("temp.jpg", "wb") as f:
                f.write(downloaded_file)
                
            img = Image.open("temp.jpg")
            caption = message.caption if message.caption else "Please solve and explain this."
            
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[caption, img],
                config={
                    "generation_config": generation_config, 
                    "system_instruction": system_instruction
                }
            )
            bot.reply_to(message, response.text)
            os.remove("temp.jpg")
            
        elif message.content_type == 'text':
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=message.text,
                config={
                    "generation_config": generation_config, 
                    "system_instruction": system_instruction
                }
            )
            bot.reply_to(message, response.text)
            
    except Exception as e:
        print(f"Error encountered: {e}")

if name == "main":
    print("Bot is starting up...")
    bot.infinity_polling()
