# RuneFinder.py
import os
import random
from urllib.error import HTTPError
import requests
import discord
from bs4 import BeautifulSoup
from blitz_crawler import BlitzCrawler

#Converts lists into string; USED:Summoners,Runes
def list_to_string(list):
    final_string=""
    for thing in list:
        final_string+=thing
        if(thing != list[-1]):
            final_string+=", "
    return final_string
        
#Converts list into fancy string; USED: Build
def list_to_build(list):
    final_string=""
    for item in list:
        final_string+=item
        if(item != list[-1]):
            final_string+=" -> "
    return final_string

def tupled_list_to_string(list):
    final_string = ""
    for order in list:
        if int(order[1]) > 65:
            final_string = order[0].upper()
            return final_string
    final_string = "Hybrid"
    return final_string


from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='`')

client = discord.Client()

@bot.command("find")
async def find(ctx, *args):
    if ctx.author.bot:
        return
    chosen_champ_and_role = args
    list_of_roles = ['top', 'mid', "adc", "support", "sup", "supp", "jungle", "jg"]
    try:
        if len(chosen_champ_and_role) != 2:
            raise TypeError
        else:
            if chosen_champ_and_role[1].lower() not in list_of_roles:
                raise ValueError
    except ValueError:
        await ctx.send("\nThat response contained a lane that does not exist. Please respond with one of the following lane options: Top, Mid, Jungle, ADC, or Support \n")
        return
    except Exception:
        await ctx.send("\nThat response was not formatted properly. Please respond with a champion and associated lane i.e. `find Ahri Mid \n")
        return
    mispelled_sup = ['sup', 'supp']
    if chosen_champ_and_role[1].lower() in mispelled_sup:
        champ_role = "Support"
    elif chosen_champ_and_role[1].lower() == 'jg':
        champ_role = "Jungle"
    else:
        list_of_proper_roles = ['Top', 'Mid', "ADC", "Jungle", "Support"]
        champ_role = list_of_proper_roles[list_of_roles.index(chosen_champ_and_role[1].lower())]
    try:
        champion_info_finder = BlitzCrawler(chosen_champ_and_role[0], champ_role)
    except HTTPError as e:
        await ctx.send("\nThere was an internal server error. Try again in 24 hours and contact the developers if the problem persists. \n" + str(e))
        return
    champion_info_finder.requested_info_builder(True, True, True, True, True, True, True)
    await ctx.send(
    "Winning Lanes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.winlane_info, 4)) +
    "\nCounter Lanes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.counterlane_info, 4)) +
    "\nStarting items: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_starting_items)) + 
    "\nSummoners: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_summoner_spells, 3)) + 
    "\nPrimary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_primary_tree, 2)) +
    "\nSecondary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_secondary_tree, 2)) +
    "\nBuild: " + list_to_build(champion_info_finder.image_name_locater(champion_info_finder.win_rate_final_items_build)) +
    "\nSkill Order: " + list_to_build(champion_info_finder.paragraph_text_locator(champion_info_finder.win_rate_skill_orders)) +
    "\nDamage Classification: " + tupled_list_to_string(champion_info_finder.div_text_locator(champion_info_finder.win_rate_damage_classification))+"\n"
    )

@bot.command("help")
async def help(ctx, *args):
    if ctx.author.bot:
        return
    ctx.send("\nIn order to use RuneFinder. Use the command `find before the a champion and its associated lane i.e. `find Ahri Mid")

bot.run(TOKEN)