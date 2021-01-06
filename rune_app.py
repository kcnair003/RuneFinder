# RuneFinder.py
import os
import random
import requests
import time
import discord
from bs4 import BeautifulSoup
from blitz_crawler import BlitzCrawler

#Prints lines in animated sequence
def delay_print(item):
    for character in item:
        print(character, end='', flush=True)
        time.sleep(0.05)

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
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='`')

client = discord.Client()



@bot.command()
async def find(ctx, *, arg):
    if str(ctx.message.author.id) == "790773102237188148": #fix plz no work
        return
    proper_response = False
    chosen_champ_and_role_cleaned = []
    while not proper_response:
        try:
            #requested_champ_and_role = input("\nType the champ and role that you would like separated with a space (i.e. !Ahri Mid)\n")
            proper_response = True
            chosen_champ_and_role_cleaned = list(map(str, arg.split(' ')))
            if len(chosen_champ_and_role_cleaned) != 2:
                raise TypeError
            else:
                list_of_roles = ['top', 'mid', "adc", "support", "sup", "supp", "jungle", "jg"]
                if chosen_champ_and_role_cleaned[1].lower() not in list_of_roles:
                    raise ValueError
        except ValueError:
            proper_response=False
            await ctx.send("\nThat response contained a lane that does not exist. Please respond with one of the following lane options: Top, Mid, Jungle, ADC, or Support \n")
        except Exception:
            proper_response=False
            await ctx.send("\nThat response was not formatted properly. Please respond with a champion and associated lane i.e. !Ahri Mid \n")
    if "!" in chosen_champ_and_role_cleaned[0]:
        champ_name = chosen_champ_and_role_cleaned[0].replace("!", '')
        chosen_champ_and_role_cleaned[0] = champ_name
    if chosen_champ_and_role_cleaned[1].lower() in 'support':
        chosen_champ_and_role_cleaned[1] = "Support"
    if chosen_champ_and_role_cleaned[1].lower() == "jg":
        chosen_champ_and_role_cleaned[1] = "Jungle"

    
    champion_info_finder = BlitzCrawler(chosen_champ_and_role_cleaned[0], chosen_champ_and_role_cleaned[1])
    champion_info_finder.requested_info_builder(True, True, True, True, True, True, True)
    await ctx.send("Starting items: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_starting_items))+"\n")
    await ctx.send("Summoners: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_summoner_spells, 3))+"\n")
    await ctx.send("Primary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_primary_tree, 2))+"\n")
    await ctx.send("Secondary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_secondary_tree, 2))+"\n")
    await ctx.send("Build: " + list_to_build(champion_info_finder.image_name_locater(champion_info_finder.win_rate_final_items_build))+"\n")
    await ctx.send("Skill Order: " + list_to_build(champion_info_finder.paragraph_text_locator(champion_info_finder.win_rate_skill_orders))+"\n")
    await ctx.send("Damage Classification: " + tupled_list_to_string(champion_info_finder.div_text_locator(champion_info_finder.win_rate_damage_classification))+"\n")


bot.run(TOKEN)