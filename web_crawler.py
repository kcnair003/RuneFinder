import requests
from bs4 import BeautifulSoup
import re

class WebCrawler():

    #This method intializes the desired champ and role in the specified page
    def __init__(self, champ_name, role):
        self.champ_name = champ_name
        self.role = role
        URL = 'https://champion.gg/champion/' + champ_name + '/' + role
        self.page = requests.get(URL)

    #This method traverses an html element to find all the underlying images and returns said list    
    def image_locater(self, image_location):
        final_images = []
        found_images = image_location.findAll("img")
        for image in found_images:
            if image:
                final_images.append(image)
        return final_images

    #This method traverses an html element to find the names for the requested object. By default, the requested object param is set to 1 for items, but can be set to 2 for runes or 3 for summoner spells
    def image_name_locater(self, image_location, requested_object=1):
        if requested_object==1:
            requested_item = 'item'
        elif requested_object==2:
            requested_item = 'rune'
        elif requested_object==3:
            requested_item = 'spell'
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

    #This method prepares the Web Scraper based on the desired information
    def requested_info_builder(self, starting_items=False, summoners_spells=False, final_items=False, primary_runes=False, secondary_runes=False):
        self.champion_highest_winrate_build_info_web_scraper().champion_highest_winrate_build_items_and_runes_web_scraper().item_builder(starting_items, summoners_spells, final_items).rune_builder(primary_runes, secondary_runes)
        return self
        
    #This method prepares the WebCrawler to find requested item information
    def item_builder(self, starting_items, summoners_spells, final_items):
        if starting_items or summoners_spells or final_items:
            self.champion_highest_winrate_build_items_web_scraper()
            if final_items:
                self.champion_highest_winrate_build_final_items_web_scraper()
            if starting_items or summoners_spells:
                self.champion_highest_winrate_build_summoner_spells_and_starting_items_web_scraper()
                if starting_items:
                    self.champion_highest_winrate_build_starting_items_web_scraper()
                if summoners_spells:
                    self.champion_highest_winrate_build_summoner_spells_web_scraper()
        return self

    #This method prepares the WebCrawler to find requested rune information
    def rune_builder(self, primary_runes, secondary_runes):
        if primary_runes or secondary_runes:
            self.champion_highest_winrate_build_runes_web_scraper()
            if primary_runes:
                self.champion_highest_winrate_build_primary_runes_web_scraper()
            if secondary_runes:
                self.champion_highest_winrate_build_secondary_runes_web_scraper()
        return self

    #This method scrapes the web page for the highest win rate build element
    def champion_highest_winrate_build_info_web_scraper(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        results = soup.find('div', class_="Columns__Column-sc-24rxii-1 kbeXNP")
        champion_info_children = results.findChildren('div', recursive=False)
        highest_win_rate_build_container = champion_info_children[1]
        highest_win_rate_build_info = highest_win_rate_build_container.find('div', class_="Inner-sc-7vmxjm-0 cpZSJT")
        self.highest_win_rate_build_info_children = highest_win_rate_build_info.findChildren('div', recursive=False)
        return self

    #This method scrapes the highest win rate build element for its items and runes
    def champion_highest_winrate_build_items_and_runes_web_scraper(self):
        self.highest_win_rate_build_items_and_runes_children = self.highest_win_rate_build_info_children[0].findChildren('div', recursive=False)
        return self

    #This method scrapes the highest win rate build items and runes for the items
    def champion_highest_winrate_build_items_web_scraper(self):
        self.highest_win_rate_build_items_children = self.highest_win_rate_build_items_and_runes_children[0].findChildren('div', recursive=False)
        return self

    #This method scrapes the highest win rate build items for its final build
    def champion_highest_winrate_build_final_items_web_scraper(self):
        self.highest_win_rate_final_items_build = self.highest_win_rate_build_items_children[2]
        return self

    #This method scrapes the highest win rate build items for its summoner spells and starting items
    def champion_highest_winrate_build_summoner_spells_and_starting_items_web_scraper(self):
        self.highest_win_rate_build_summoner_spells_and_starting_items_children = self.highest_win_rate_build_items_children[0].findChildren('div', recursive=False)
        return self

    #This method scrapes the highest win rate build summoner spells and starting items for its summoner spells
    def champion_highest_winrate_build_summoner_spells_web_scraper(self):
        self.highest_win_rate_build_summoner_spells = self.highest_win_rate_build_summoner_spells_and_starting_items_children[0]
        return self

    #This method scrapes the highest win rate build summoner spells and starting items for its starting items
    def champion_highest_winrate_build_starting_items_web_scraper(self):
        self.highest_win_rate_build_starting_items = self.highest_win_rate_build_summoner_spells_and_starting_items_children[2]
        return self

    #This method scrapes the highest win rate build items and runes for its runes
    def champion_highest_winrate_build_runes_web_scraper(self):
        highest_win_rate_build_runes_children = self.highest_win_rate_build_items_and_runes_children[1].findChildren('div', recursive=False)
        highest_win_rate_runes_children = highest_win_rate_build_runes_children[0].findChildren('div', recursive=False)
        self.highest_win_rate_runes_tree_children = highest_win_rate_runes_children[0].findChildren('div', recursive=False)
        return self
    
    #This method scrapes the highest win rate build runes for its primary rune tree
    def champion_highest_winrate_build_primary_runes_web_scraper(self):
        self.highest_win_rate_runes_primary_tree = self.highest_win_rate_runes_tree_children[0]
        return self
    
    #This method scrapes the highest win rate build runes for its secondary rune tree
    def champion_highest_winrate_build_secondary_runes_web_scraper(self):
        self.highest_win_rate_runes_secondary_tree = self.highest_win_rate_runes_tree_children[1]
        return self

    #This method scrapes the highest win rate build for its skill order info
    def champion_highest_winrate_build_skill_order(self):
        self.highest_win_rate_build_skill_order = self.highest_win_rate_build_info_children[2]
        return self
