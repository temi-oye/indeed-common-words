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

# searches a generic term (software in this case) and goes through all the pages and graphs the most common words found (while filtering out stopwords)
# random sleeps to prevent too many requests being sent in a short space of time

word_frequency = {}

def get_words_from_file(file_name):
  list_of_words = []
  with open(file_name, 'r', encoding="utf8") as file:
    for line in file:
      list_of_words.extend(line.split())
  return list_of_words

def get_stop_words():
  save_path = r"path to folder\NLP"
  file_name = "stop_words_english.txt"
  complete_name = os.path.join(save_path, file_name)
  addtional_stop_words = get_words_from_file(complete_name)
  
  return set(stopwords.words("english") + addtional_stop_words)

def get_word_frequency(word_dict, string, stop_words):
  words = re.split(r"\W+", string)

  common_technologies = get_words_from_file(r"path to text file\common-technologies.txt")
  
  for word in words:
    if(word.lower() in word_dict and word not in stop_words and word in common_technologies):
      word_dict[word.lower()] += 1
    elif word not in stop_words and word in common_technologies:
      word_dict[word.lower()] = 1


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=r"path to driver\chromedriver.exe", options=options)

def search_this_query_indeed(query):
  driver.get("https://ie.indeed.com/")

  search_box = driver.find_element(By.ID, "text-input-what")
  search_box.send_keys(query)
  sleep(randint(1, 4))
  search_box.send_keys(Keys.ENTER)

search_this_query_indeed("software")

def get_word_frequency_for_page(word_dict):
  jobs =  driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

  for i in range(0, len(jobs)):
    sleep(randint(1, 3))
    driver.execute_script("arguments[0].click();", jobs[i])

    sleep(randint(1, 4))

    driver.switch_to.frame(driver.find_elements(By.TAG_NAME,"iframe")[0])
    job_desc = driver.find_element(By.CLASS_NAME, "jobsearch-JobComponent-embeddedBody")

    sleep(randint(2, 5))

    stop_words = get_stop_words()

    get_word_frequency(word_dict, job_desc.text, stop_words)

    driver.switch_to.parent_frame()

driver.implicitly_wait(5)

def go_to_next_page(is_next_page):
  if is_next_page:
    next_page_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next']")
    driver.execute_script("arguments[0].click();", next_page_btn)


is_next_page = True

while is_next_page:
  sleep(randint(1, 5))

  get_word_frequency_for_page(word_frequency)

  is_next_page = driver.find_elements(By.XPATH, "//a[@aria-label='Next']")
  go_to_next_page(is_next_page)
  # is_next_page = False


def make_most_frequent_words_barchart(word_dict):
  top_words_dict = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:20])

  words = list(top_words_dict.keys())
  frequencies = list(top_words_dict.values())

  plt.barh(words, frequencies)
  plt.show()

make_most_frequent_words_barchart(word_frequency)

driver.quit()

