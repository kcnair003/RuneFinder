import requests
import time
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

#Requests for a set of answers from the range of starting value to the expected max
matchups = winlane = counterlane = winrate = items = spells = build = main_runes = side_runes = skills = damage = False
def request_champ_and_role():
    global matchups, winlane, counterlane, winrate, items, spells, build, main_runes, side_runes, skills, damage
    proper_response = False
    chosen_champ_and_role_cleaned = []
    while not proper_response:
        try:
            requested_champ_and_role = input("\nType the champ and role that you would like separated with a space (i.e. !Ahri Mid)\n")
            proper_response = True
            chosen_champ_and_role_cleaned = list(map(str, requested_champ_and_role.split(' ')))
            if len(chosen_champ_and_role_cleaned) == 1 or len(chosen_champ_and_role_cleaned) > 4:
                raise TypeError
            else:
                list_of_roles = ['top', 'mid', "adc", "support", "sup", "supp", "jungle", "jg"]
                list_of_third_argument = ['winning', 'counter', 'counters', 'starting', 'summoners', 'secondary', 'build', 'skill', 'damage']
                
                if chosen_champ_and_role_cleaned[2].lower() not in list_of_roles:
                    raise ValueError
                if ((len(chosen_champ_and_role_cleaned) > 3) and (chosen_champ_and_role_cleaned[3].lower() not in list_of_third_argument)):
                    raise ValueError
        except ValueError:
            proper_response=False
            delay_print("\nThat response contained a lane that does not exist. Please respond with one of the following lane options: Top, Mid, Jungle, ADC, or Support \n")
        except Exception:
            proper_response=False
            delay_print("\nThat response was not formatted properly. Please respond with a champion and associated lane i.e. !Ahri Mid \n")
    if "!" in chosen_champ_and_role_cleaned[0]:
        champ_name = chosen_champ_and_role_cleaned[0].replace("!", '')
        chosen_champ_and_role_cleaned[1] = champ_name
    if chosen_champ_and_role_cleaned[2].lower() in 'support':
        chosen_champ_and_role_cleaned[2] = "Support"
    if chosen_champ_and_role_cleaned[2].lower() == "jg":
        chosen_champ_and_role_cleaned[2] = "Jungle"
    if len(chosen_champ_and_role_cleaned) == 3:
        matchups = winlane = counterlane = winrate = items = spells = build = main_runes = side_runes = skills = damage = True
    return chosen_champ_and_role_cleaned

#This is the main method that runs the code
def main():
    user_response = request_champ_and_role()
    try:
        champion_info_finder = BlitzCrawler(user_response[1], user_response[2])
        champion_info_finder.requested_info_builder(matchups, winlane, counterlane, winrate, items, spells, build, main_runes, side_runes, skills, damage)
        print("Winning Lanes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.winlane_info, 4))+"\n")
        print("Counter Lanes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.counterlane_info, 4))+"\n")
        print("Starting items: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_starting_items))+"\n")
        print("Summoners: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_build_summoner_spells, 3))+"\n")
        print("Primary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_primary_tree, 2))+"\n")
        print("Secondary Runes: " + list_to_string(champion_info_finder.image_name_locater(champion_info_finder.win_rate_runes_secondary_tree, 2))+"\n")
        print("Build: " + list_to_build(champion_info_finder.image_name_locater(champion_info_finder.win_rate_final_items_build))+"\n")
        print("Skill Order: " + list_to_build(champion_info_finder.paragraph_text_locator(champion_info_finder.win_rate_skill_orders))+"\n")
        print("Damage Classification: " + tupled_list_to_string(champion_info_finder.div_text_locator(champion_info_finder.win_rate_damage_classification))+"\n")
    except Exception as e:
        print(e)


main()