import requests
import time
from bs4 import BeautifulSoup
from web_crawler import WebCrawler

#Prints lines in animated sequence
def delay_print(item):
    for character in item:
        print(character, end='', flush=True)
        time.sleep(0.05)

#Requests for a set of answers from the range of starting value to the expected max
def request_champ_and_role():
    proper_response = False
    chosen_champ_and_role_cleaned = []
    while not proper_response:
        try:
            requested_champ_and_role = input("\nType the champ and role that you would like separated with a space (i.e. !Ahri Mid)\n")
            proper_response = True
            chosen_champ_and_role_cleaned = list(map(str, requested_champ_and_role.split(' ')))
            if len(chosen_champ_and_role_cleaned) != 2:
                raise TypeError
            else:
                list_of_roles = ['top', 'mid', "adc", "support", "jungle", "jg"]
                if chosen_champ_and_role_cleaned[1].lower() not in list_of_roles:
                    raise ValueError
        except ValueError:
            proper_response=False
            delay_print("\nThat response contained a lane that does not exist. Please respond with one of the following lane options: Top, Mid, Jungle, ADC, or Support \n")
        except Exception:
            proper_response=False
            delay_print("\nThat response was not formatted properly. Please respond with a champion and associated lane i.e. !Ahri Mid \n")
    if "!" in chosen_champ_and_role_cleaned[0]:
        champ_name = chosen_champ_and_role_cleaned[0].replace("!", '')
        chosen_champ_and_role_cleaned[0] = champ_name
    if chosen_champ_and_role_cleaned[1].lower() in 'support':
        chosen_champ_and_role_cleaned[1] = "Support"
    if chosen_champ_and_role_cleaned[1].lower() == "jg":
        chosen_champ_and_role_cleaned[1] = "Jungle"
    return chosen_champ_and_role_cleaned

#This is the main method that runs the code
def main():
    user_response = request_champ_and_role()
    champion_info_finder = WebCrawler(user_response[0], user_response[1])
    champion_info_finder.requested_info_builder(True, True, True, True, True)
    print(champion_info_finder.image_locater(champion_info_finder.highest_win_rate_final_items_build))


main()