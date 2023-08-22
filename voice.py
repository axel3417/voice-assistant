import threading
import speech_recognition as sr
import re
from discord_webhook import DiscordWebhook

WEBHOOK_URL = 'your_discord_webhook_url'                                                                    #Enter your discord webhook

def send_webhook(content):
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=content)
    response = webhook.execute()

    if response.status_code == 204:
        print("Message send.")
    else:
        print("Error.")

def main():
    recognizer = sr.Recognizer()

    def listen_for_commands():
        while True:
            with sr.Microphone() as source:
                print("Tell me something...")
                audio = recognizer.listen(source)

                try:
                    text = recognizer.recognize_google(audio, language="us-US")                             #Enter your language
                    if "done" in text.lower():
                        send_webhook("Done.")
                        print("Done.")
                    elif "add" in text.lower() and "to the list" in text.lower():
                        match = re.search(r"add\s+(.*?)\s+to the list", text, re.IGNORECASE)
                        if match:
                            product = match.group(1)
                            send_webhook(f"add '{product}' to the list.")
                            print(f"add '{product}' to the list.")
                        else:
                            print("product not found.")
                    else:
                        print("Command not founded.")
                except sr.UnknownValueError:
                    print("I don't understand what you say.")
                except Exception as e:
                    print(f"Errore: {e}")

    thread = threading.Thread(target=listen_for_commands)
    thread.daemon = True
    thread.start()

    input("press enter to terminate...")

if __name__ == "__main__":
    main()
