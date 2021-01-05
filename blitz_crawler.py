import requests
from bs4 import BeautifulSoup
import re

class BlitzCrawler():

    #Creates the BlitzCrawler and gets the URL
    def __init__(self, champ_name, role):
        self.champ_name = champ_name
        self.role = role
        URL = 'https://champion.gg/champion/' + champ_name + '/' + role
        self.page = requests.get(URL)

    #Prepares the Web Scraper based on the desired information
    def requested_info_builder(self, starting_items=False, summoners_spells=False, final_items=False, primary_runes=False, secondary_runes=False):
        self.winrate_build_scraper()
        if starting_items or summoners_spells or final_items:
            self.winrate_build_items_web_scraper()
            if starting_items or summoners_spells:
                self.winrate_build_summoner_spells_and_starting_items_web_scraper()
        if primary_runes or secondary_runes:
            self.winrate_build_runes_web_scraper()
        return self

    #Finds the images and returns their descriptions    
    def image_locater(self, image_location):
        final_images = []
        found_images = image_location.findAll("img")
        for image in found_images:
            if image:
                final_images.append(image)
        return final_images

    #Find the names for the requested object. Default:items
    def image_name_locater(self, image_location, requested_object=1):
        if requested_object==1:
            requested_item = 'item'
        elif requested_object==2:
            requested_item = 'rune'
        elif requested_object==3:
            requested_item = 'spell' #summoner spell
        else:
            raise ValueError
        final_images = []
        found_images = image_location.findAll("img")
        for image in found_images:
            if image:
                try:
                    image_name = re.search('<' + requested_item + 'name>(.+?)</' + requested_item + 'name>',image['data-tip']).group(1)
                    final_images.append(image_name)
                except AttributeError:
                    pass
        return final_images
    
    #Scrapes web page for highest win rate build div container
    def winrate_build_scraper(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        results = soup.find('div', class_="Columns__Column-sc-24rxii-1 kbeXNP")
        info_children = results.findChildren('div', recursive=False)
        win_rate_build_container = info_children[1]
        win_rate_build_info = win_rate_build_container.find('div', class_="Inner-sc-7vmxjm-0 cpZSJT")
        self.win_rate_build_info_children = win_rate_build_info.findChildren('div', recursive=False)
        self.win_rate_build_items_and_runes_children = self.win_rate_build_info_children[0].findChildren('div', recursive=False)
        return self

    #Scrapes highest win rate build summoner spells, starting items, and final items div container
    def winrate_build_items_web_scraper(self):
        self.win_rate_build_items_children = self.win_rate_build_items_and_runes_children[0].findChildren('div', recursive=False)
        self.win_rate_final_items_build = self.win_rate_build_items_children[2]
        return self

    #Scrapes highest win rate build div container for its summoner spells and starting items
    def winrate_build_summoner_spells_and_starting_items_web_scraper(self):
        self.win_rate_build_summoner_spells_and_starting_items_children = self.win_rate_build_items_children[0].findChildren('div', recursive=False)
        self.win_rate_build_summoner_spells = self.win_rate_build_summoner_spells_and_starting_items_children[0]
        self.win_rate_build_starting_items = self.win_rate_build_summoner_spells_and_starting_items_children[2]
        return self

    #Scrapes highest win rate build runes div container for runes
    def winrate_build_runes_web_scraper(self):
        win_rate_build_runes_children = self.win_rate_build_items_and_runes_children[1].findChildren('div', recursive=False)
        win_rate_runes_children = win_rate_build_runes_children[0].findChildren('div', recursive=False)
        self.win_rate_runes_tree_children = win_rate_runes_children[0].findChildren('div', recursive=False)
        self.win_rate_runes_primary_tree = self.win_rate_runes_tree_children[0] #Primary Runes
        self.win_rate_runes_secondary_tree = self.win_rate_runes_tree_children[1] #Secondary Runes
        return self

    #Scrapes highest win rate build div container for skill order info
    def winrate_build_skill_order(self):
        self.win_rate_build_skill_order = self.win_rate_build_info_children[2]
        return self
