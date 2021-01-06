# RuneFinder.py
import os
import random
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

#Converts tupled list for damage into a specific classification
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
    chosen_champ_and_role_cleaned = args
    list_of_roles = ['top', 'mid', "adc", "jungle", "support"]
    try:
        if len(chosen_champ_and_role_cleaned) != 2:
            raise TypeError
        else:
            if chosen_champ_and_role_cleaned[1].lower() not in list_of_roles:
                raise ValueError
    except ValueError:
        await ctx.send("\nThat response contained a lane that does not exist. Please respond with one of the following lane options: Top, Mid, Jungle, ADC, or Support \n")
        return
    except Exception:
        await ctx.send("\nThat response was not formatted properly. Please respond with a champion and associated lane i.e. !find Ahri Mid \n")
        return
    list_of_proper_roles = ['Top', 'Mid', "ADC", "Jungle", "Support"]
    champ_role = list_of_proper_roles[list_of_roles.index(chosen_champ_and_role_cleaned[1].lower())]
    champion_info_finder = BlitzCrawler(chosen_champ_and_role_cleaned[0], champ_role)
    champion_info_finder.requested_info_builder(True, True, True, True, True, True, True)
    await ctx.send("Starting items: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_starting_items)) + 
    "\nSummoners: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_summoner_spells, 3)) + 
    "\nPrimary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_primary_tree, 2)) +
    "\nSecondary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_secondary_tree, 2)) +
    "\nBuild: " + list_to_build(champion_info_finder.image_name_locater(champion_info_finder.win_rate_final_items_build)) +
    "\nSkill Order: " + list_to_build(champion_info_finder.paragraph_text_locator(champion_info_finder.win_rate_skill_orders)) +
    "\nDamage Classification: " + tupled_list_to_string(champion_info_finder.div_text_locator(champion_info_finder.win_rate_damage_classification))+"\n")

bot.run(TOKEN)