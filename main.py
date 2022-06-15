import requests
from time import sleep
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
from random import randint
import operator
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_words_from_file(file_name):
  list_of_words = []
  with open(file_name, 'r', encoding="utf8") as file:
    for line in file:
      list_of_words.append(line.strip())
  return list_of_words

def search_this_query_indeed(query):
  search_box = driver.find_element(By.ID, "text-input-what")
  search_box.send_keys((Keys.CONTROL,"a", Keys.DELETE))
  search_box.send_keys(query)
  sleep(randint(1, 4))
  search_box.send_keys(Keys.ENTER)

def make_most_frequent_words_barchart(word_dict):
  top_words_dict = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:20])

  words = list(top_words_dict.keys())
  frequencies = list(top_words_dict.values())

  plt.barh(words, frequencies)
  plt.show()

def get_number_of_jobs():

  pages_and_jobs = driver.find_elements(By.ID, "searchCountPages")

  number_of_jobs = int(re.search(r"(?<=of\s)((\d+,\d+)|\d+)", pages_and_jobs[0].text.replace(",",""))[0]) if len(pages_and_jobs) > 0 else 0

  return number_of_jobs

word_frequency = {}
common_technologies = get_words_from_file(r"common-technologies.txt")

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=r"Path to driver\chromedriver.exe", options=options)
driver.get("https://ie.indeed.com/")

for technology in common_technologies:
  search_this_query_indeed(technology)
  word_frequency[technology] = get_number_of_jobs()
  sleep(randint(1, 4))

driver.quit()

make_most_frequent_words_barchart(word_frequency)
