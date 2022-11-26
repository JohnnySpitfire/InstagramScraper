from instagrapi import Client

cl = Client()
cl.login("", "")

messages = cl.direct_messages('340282366841710300949128299951790614236', 10)
messages = [message for message in messages if message.item_type == "voice_media"]
print(messages)