import requests
from bs4 import BeautifulSoup

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
    def champion_highest_winrate_build_final_build_web_scraper(self):
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
        self.highest_win_rate_build_summoner_spells = self.highest_win_rate_build_summoner_spells_and_starting_items_children[2]
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
