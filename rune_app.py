# RuneFinder.py
import os
import random
import requests
import time
from bs4 import BeautifulSoup
from blitz_crawler import BlitzCrawler

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='`')

@bot.command()
async def find(ctx, *, arg):
    await ctx.send(arg)

bot.run(TOKEN)