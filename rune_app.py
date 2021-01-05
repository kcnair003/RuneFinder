# rune_app.py
#import os
#from dotenv import load_dotenv
#TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client()

#@client.event
#async def on_ready():
#    print(f'{client.user} has connected to Discord!')

#client.run(TOKEN)



import discord
client = discord.Client()
Token=''
@client.event
async def onmessage(message):
    message.content.lower()
    if message.author == client.user:
        return
    if message.content.startswith("Hello"):
        await message.channel.send("Hello, I am a test bot.")
    
client.run(Token)
