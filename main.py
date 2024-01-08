import logging
import csv
import json
import requests
from argparse import ArgumentParser
from tqdm import tqdm
from bs4 import BeautifulSoup
from time import time


def extract_data(html_fragment:str):
''' extracts all relevant data from html fragment '''
# use beautifulsoup to parse? use regex?


def has_error(response:str):
''' returns true if there is an issue with the response '''

  if response.status_code != 200: # requires raw response... maybe convert to "is None" check (and return None when status code != 200)?
    return True
  if response['success'] != '1':  # requires json parsing...
    return True

  return False


def get_recommendations(curator:str, start:int, count:int):  # do we need option to inject session?
''' wraps steam api for requesting a curator's recommendations '''

  # just need some nice way of writing this...
  base_url = f"https://store.steampowered.com/curator/{curator}/ajaxgetfilteredrecommendations/"
  params = f"?query&start={start}&count={count}&dynamic_data=&tagids=&sort=recent&app_types=&curations=&reset=false"
  query = base_url + params
  try:

    response = requests.get(query)
    logging.debug("response received:\n%s", response)

    json_object = json.loads(response)
    logging.debug("json parsing successful")

  except Exception as ex:
    pass

  return json_object


def scrape_recommendations(curator:str):
''' makes all requests to scrape curator reviews '''

  start = 0
  count = 10

  while True:

    json_object = get_recommendations(curator, start, count)

    # check for issues with response
    if has_error(json_object):
      # retry? handle error? raise error?
      raise RuntimeError("Ran into issue with response")  # add stacktrace

    # return response as an element of a generator
    yield json_object

    # check if done
    if (start + count) >= json_object['total_count']:  # requires json parsing...
      break

    # prepare for next request
    start += count

    # insert random delay of approx 0.5s
    time.sleep(0.5)

  return # end generator


def run(**kwargs):

  #try:
  # for response_object in scrape_recommendations(curator):
  #   recommendation_batch = extract_data(response_object.results_html)
  #   write lines to csv
  #except:

  pass


if __name__ == "__main__":

  # need an argument for 'curator'

  parser = argparse.ArgumentParser()
  args = parser.parse_args()
  run(**args) # to_dict()??

