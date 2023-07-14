from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np

chrome_options = Options()
chrome_options.add_argument('__headless')
chrome_options.add_argument("--no-sandbox")

playlists = 'https://www.youtube.com/@ItchyBoots/playlists'

driver = webdriver.Chrome(options = chrome_options)
driver.get(playlists)

seasons = driver.find_elements(By.LINK_TEXT,
                             'View full playlist')

season_list = []
for s in seasons:
    url = s.get_attribute('href')
    season_list.append(url)

driver = webdriver.Chrome(options = chrome_options)
itchy_boots = {}
for s in season_list:
    driver.implicitly_wait(3)
    driver.get(s)
    season =  driver.find_element(By.CSS_SELECTOR, 
                                  'yt-dynamic-sizing-formatted-string').text
    episodes = driver.find_elements(By.CSS_SELECTOR, 
                             'h3[class="style-scope ytd-playlist-video-renderer"]')
    episode_texts=[]
    for e in episodes:
        episode_texts.append(e.get_attribute('aria-label'))
    itchy_boots[season] = episode_texts


driver.quit()


def to_dict_data(episode, season, data_list):
    """
    Dividing areas to a dicts list 
    """
    s1 = episode.split('by Itchy Boots')
    title = s1[0]
    s2 = s1[1].split('ago')
    date = s2[0]
    s3 = s2[1].split('minute')
    time = s3[0]
    rating= s3[1]
    data_list.append({'season':season,
                      'episode':title,
                      'date':date,
                      'time':time,
                      'rating':rating})
itchies = []
for season in itchy_boots.keys():
    for episode in itchy_boots[season]:
        to_dict_data(episode, season, itchies)

raw_data = pd.DataFrame(itchies)

raw_data.to_csv('datasets/itchy_boots_raw.csv')