from stream_chat import StreamChat
import asyncio

chat = StreamChat(api_key="5ee4bvpd9hk5", api_secret="va9mfdyrqgdcj3ktz2d46bghs3h6fvk8dynnvv2s9uqqy4z6drbsc2w8df9g8kn7")

# add a user
chat.update_user({"id": "5ec26c75dde4210042211259", "name": "Chuck"})
token = chat.create_token("5ec26c75dde4210042211259")
print(token)

# create a channel about kung-fu
channel = chat.channel("messaging", "5ec26c75dde4210042211259")
channel.create("5ec26c75dde4210042211259")


msg = channel.send_message({"text": "what are the scholarships"}, "Chuck")

   



