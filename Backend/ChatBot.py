import os
import requests
import whisper
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

BOT_TOKEN = "7914632716:AAGc5sUFLwXXP9_QiWCmlV2zjmCfvdcRUU4"
CHAT_ID = "6234213967"

EMERGENCY_KEYWORDS = [
    "help", "sos", "emergency", "please help", "i'm in danger",
    "send help", "urgent help", "call the police", "danger",
    "save me", "get me out of here", "assist me", "i'm being followed",
    "somebody's watching me", "i am being kidnapped", "i fear for my safety"
]
safety_bot = ChatBot("WomenSafetyBot")
trainer = ChatterBotCorpusTrainer(safety_bot)
trainer.train("chatterbot.corpus.english")

custom_trainer = ListTrainer(safety_bot)
training_data = [
   "Is this area safe?",
    "Please share your location. I will check crime reports and suggest a safe route.",

    "What should I do if I feel unsafe?",
    "Stay in a public place, call a trusted contact, or use the SOS feature for immediate help.",

    "Where is the nearest police station?",
    "I can find the nearest police station based on your location. Please enable GPS.",

    "How can I call for help silently?",
    "You can use the silent SOS feature in the app, or press a hidden button inside a common app.",

    "Can I share my location with emergency contacts?",
    "Yes, you can enable real-time location sharing with your emergency contacts.",

    "How do I use the SOS feature?",
    "Press the SOS button in the app, and it will send alerts to emergency contacts and authorities.",

    "What should I do if someone is following me?",
    "Stay in a crowded area, enter a nearby shop, call a trusted contact, or use the SOS button.",

    "How can I identify a safe taxi or ride service?",
    "Always check the driver’s ID, share your ride details with someone you trust, and verify the vehicle's number.",

    "What are some self-defense techniques?",
    "Aim for the attacker's weak spots—eyes, throat, groin. Carry a personal safety alarm or pepper spray.",

    "Who can I call in an emergency?",
    "You can call 112 (Emergency), 1091 (Women’s Helpline), or your local police station.",

    "Are there any women-only transport services?",
    "Yes, some cities have women-only cabs or metro coaches. Check local transport options.",

    "What should I do if I get lost in an unfamiliar place?",
    "Stay calm, look for a well-lit public area, ask help from authorities, or use maps for guidance.",

    "How do I report harassment?",
    "You can report harassment to local authorities, women’s helpline, or through online police portals.",

    "Is it safe to go out alone at night?",
    "Try to avoid isolated areas, stay alert, and keep a trusted contact informed of your location.",

    "How can I discreetly seek help in a dangerous situation?",
    "Use coded messages to inform someone you trust, or act like you are calling a friend while sharing details.",

    "What should I do if my phone battery is low and I need help?",
    "Find a public place with charging stations or ask for help at a nearby shop or police station.",

    "Are there any mobile apps for women's safety?",
    "Yes, apps like bSafe, My Safetipin, and Noonlight provide safety features like SOS alerts and tracking.",

    "How can I secure my home against intruders?",
    "Install strong locks, security cameras, and motion-detection lights. Keep emergency numbers handy.",

    "What should I do if a stranger is making me uncomfortable?",
    "Trust your instincts, maintain distance, move towards a crowded area, and be ready to call for help.",

    "Can I carry self-defense tools?",
    "Yes, items like pepper spray, a whistle, or a personal alarm can help in emergencies.",

    "What is the best way to stay safe while jogging alone?",
    "Run in well-lit, busy areas, carry a safety alarm, and avoid wearing headphones at high volume.",

    "What are the warning signs of a dangerous situation?",
    "Unusual behavior, someone following you, or unwanted attention—trust your instincts and take action.",

    "How can I prevent online harassment?",
    "Use strong passwords, enable privacy settings, block/report offenders, and avoid sharing personal details.",

    "What should I do if I receive threats online?",
    "Take screenshots, report to platform moderators, block the user, and if serious, report to cyber police.",

    "How can I travel safely in public transport?",
    "Stay near other passengers, avoid empty compartments, and inform someone of your travel details.",

    "What should I do if someone is harassing me at work?",
    "Report to HR, keep records of incidents, and seek legal advice if necessary.",
]
custom_trainer.train(training_data)

def send_sos_alert():
    message = "🚨 **EMERGENCY ALERT!** Someone needs urgent help! 🚨\nLive location is being shared..."
    text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"

    text_response = requests.get(text_url)
    if text_response.status_code == 200:
        print("🚨 Telegram alert sent successfully!")
    else:
        print("⚠️ Failed to send alert message.")

    latitude, longitude = 17.5473, 78.4041
    location_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation?chat_id={CHAT_ID}&latitude={latitude}&longitude={longitude}"

    location_response = requests.get(location_url)
    if location_response.status_code == 200:
        print("📍 Live location sent successfully!")
    else:
        print("⚠️ Failed to send live location.")


def chatbot_response(user_input):
    user_input = user_input.lower()

    for keyword in EMERGENCY_KEYWORDS:
        if keyword in user_input:
            send_sos_alert()
            return "🚨 **Emergency alert triggered! Stay strong, help is coming!**"

    return safety_bot.get_response(user_input)


def voice_chatbot(audio_file):
    model = whisper.load_model("base")
    text = model.transcribe(audio_file)["text"]

    print(f"You (voice): {text}")
    response = chatbot_response(text)
    print(f"Bot: {response}")


while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: Stay safe! Goodbye! 🛡️")
        break
    response = chatbot_response(user_input)
    print(f"Bot: {response}")
