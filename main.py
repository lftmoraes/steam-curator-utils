import csv
import json
import requests
from argparse import ArgumentParser
from tqdm import tqdm
from bs4 import BeautifulSoup

def extract_data(request):
''' extracts all relevant data from raw request '''
# response is in JSON format
# "results_html" attribute is an HTML string

def scrape_reviews(curator:str):
''' makes all requests to scrape curator reviews '''
  start = 0
  count = 10
  while True:

    query = f"https://store.steampowered.com/curator/{curator}/ajaxgetfilteredrecommendations/?query&start={start}&count={count}&dynamic_data=&tagids=&sort=recent&app_types=&curations=&reset=false"
    # make request
    response = requests.get(query)  # abstract to handle exceptions
    # could be made into a yield

    # check if done
    if start+count > response['total_count']:
      break

    # prepare for next request
    start += count

    # insert random delay of approx 0.5s

  return # reviews?

def run(**kwargs):

  #try:
  # for each review_batch in scrape_reviews():
  #   write lines to csv
  #except:

  pass

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  args = parser.parse_args()
  run(**args) # to_dict()??

