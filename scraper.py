import logging
import csv
import json
import requests
from argparse import ArgumentParser
from tqdm import tqdm
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime


logging.getLogger().setLevel(logging.DEBUG)


HEADER = ["game", "link", "review_date", "review_type", "review_text"]


def extract_recommendations(html_fragment:str):
  ''' extracts all relevant data from html fragment containing recommendations '''
  # use beautifulsoup to parse? use regex?

  soup = BeautifulSoup(html_fragment, features="html.parser")
  logging.debug(soup.prettify())
  
  recommendations = []
  for recommendation_fragment in soup.div.find_all("div", recursive=False):
     game = recommendation_fragment.find("img").get("alt")
     link = recommendation_fragment.find(class_="recommendation_link").get("href")
     review_date = recommendation_fragment.find(class_="curator_review_date").string  # do we parse?
     #review_type = recommendation_fragment.find(class_="color_informational").string
     review_text = str(recommendation_fragment.find(class_="recommendation_desc").string).strip()

     review_type = "Recommended" if recommendation_fragment.find(class_="color_recommended") is not None else "Informational" if recommendation_fragment.find(class_="color_informational") is not None else "Not Recommended"
     
     recommendations.append({'game':game, 'link':link, 'review_date':review_date, 'review_type':review_type, 'review_text':review_text})
     
  return recommendations  # as list of dicts?


#def has_error(response:str):
#''' returns true if there is an issue with the response '''
#
#  if response.status_code != 200: # requires raw response... maybe convert to "is None" check (and return None when status code != 200)?
#    return True
#  if response['success'] != '1':  # requires json parsing...
#    return True
#
#  return False


def get_filtered_recommendations(curator:str, start:int, count:int):  # do we need option to inject session?
  ''' wraps steam api for requesting curator recommendations '''

  # just need some nice way of writing this...
  base_url = f"https://store.steampowered.com/curator/{curator}/ajaxgetfilteredrecommendations/"
  params = f"?query&start={start}&count={count}&dynamic_data=&tagids=&sort=recent&app_types=&curations=&reset=false"
  query = base_url + params

  logging.debug("query: %s", query)

  try:

    response = requests.get(query)
    logging.debug("response received:\n%s", response.text)

    json_object = None
    if response.status_code == 200:
      json_object = json.loads(response.text)
      logging.debug("json parsing successful")
    else:
      raise RuntimeError("Ran into issue with response")  # add stacktrace

  except Exception as ex:
    raise RuntimeError("Ran into an issue") from ex

  return json_object


def scrape_recommendations(curator:str):
  ''' makes a series of requests to scrape all recommendations of a curator '''

  start = 1
  count = 10

  while True:

    response_object = get_filtered_recommendations(curator, start, count)

    # check for issues with response
    if response_object['success'] != '1':  # success==2 seems to be "Curator not found" or some catch-all that includes it
      # retry? handle error? raise error?
      logging.debug("success!=1")
      #raise RuntimeError("Ran into issue with response")  # add stacktrace

    # return response as an element of a generator
    yield response_object

    # check if done
    if (start + count) >= response_object['total_count']:  # requires json parsing...
      break

    # prepare for next request
    start += count

    # insert random delay of approx 0.5s
    sleep(0.5)

  return # end generator


def run(curator):

  try:

    with open(f"output_{curator}_{datetime.now().timestamp()}.csv", "w") as csvfile:  # want "scrape_<curator>_<rundate>.csv"
      writer = csv.writer(csvfile)
      writer.writerow(HEADER)

      for response_object in scrape_recommendations(curator):
        recommendation_batch = extract_recommendations(response_object["results_html"])

        for recommendation in recommendation_batch:
          writer.writerow(recommendation.values())
          #write lines to csv

  # except requests.exceptions.ConnectionError as ex: RETRY
  except Exception as ex:
    raise RuntimeError("Something went wrong") from ex


if __name__ == "__main__":

  # need an argument for 'curator'

  #parser = argparse.ArgumentParser()
  #args = parser.parse_args()
  #run(**args) # to_dict()??

  pass
