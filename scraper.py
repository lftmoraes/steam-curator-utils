import logging
import csv
import json
import requests
import traceback
#from argparse import ArgumentParser
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
#from random import random


#logging.getLogger().setLevel(logging.DEBUG)
#logging.getLogger().setLevel(logging.INFO)


HEADER = ["game", "link", "review_date", "review_type", "review_text", "review_readmore"]
MAX_RETRIES = 3
TIMEOUT = 60


def extract_recommendations(html_fragment:str) -> list[dict[str,str]]:
  ''' extracts all relevant data from html fragment containing recommendations '''

  soup = BeautifulSoup(html_fragment, features="html.parser")
  logging.debug(soup.prettify())
  
  recommendations = []
  for recommendation_fragment in soup.div.find_all("div", recursive=False):
    game = recommendation_fragment.find("img").get("alt")
    link = recommendation_fragment.find(class_="recommendation_link").get("href")
    review_date = recommendation_fragment.find(class_="curator_review_date").string  # do we parse?
    review_text = str(recommendation_fragment.find(class_="recommendation_desc").string).strip()

    review_type = "Recommended" if recommendation_fragment.find(class_="color_recommended") is not None else "Informational" if recommendation_fragment.find(class_="color_informational") is not None else "Not Recommended"

    review_readmore = recommendation_fragment.find(class_="recommendation_readmore")
    if review_readmore is not None:
      review_readmore = review_readmore.a.get("href")
    
    recommendations.append({'game':game, 'link':link, 'review_date':review_date, 'review_type':review_type, 'review_text':review_text, 'review_readmore':review_readmore})
     
  return recommendations


def get_filtered_recommendations(curator:str, start:int, count:int, tagids='', curations='', session=None) -> object:
  ''' wraps steam api for requesting curator recommendations '''
  '''
    start - Position to start pagination. First element is 0.
    count - Number of entries to retrieve. Typical is 10. Most likely works up to 100.
    tagids - Comma separated list of tag ids to filter by. Separate with '%2C'
    curations - Comma separated list of values in {0,1,2} that correspond to RECOMMENDED, NOT-RECOMMENDED, INFORMATIONAL to filter by. Separate with '%2C'.
  '''

  # includes unused params present in web ui requests
  base_url = f"https://store.steampowered.com/curator/{curator}/ajaxgetfilteredrecommendations/"
  params = f"?query&start={start}&count={count}&dynamic_data=&tagids={tagids}&sort=recent&app_types=&curations={curations}&reset=false"

  query = base_url + params
  logging.info("query: %s", query)

  response = None
  if session is not None:
    response = session.get(query, timeout=TIMEOUT)
  else:
    response = requests.get(query, timeout=TIMEOUT)
  logging.debug("response received:\n%s", response.text)

  if response.status_code != 200:  # break into different exceptions depending on status code? some may be recoverable
    raise RuntimeError(f"Request error. Status code {response.status_code}.")

  json_object = json.loads(response.text)

  if json_object['success'] != 1:  # success==2 seems to be "Curator not found" or some catch-all that includes it
    raise RuntimeError(f"API error. API code {json_object['success']}.")

  return json_object


def scrape_recommendations(curator:str):
  ''' makes a series of requests to scrape all recommendations of a curator '''

  start = 0
  count = 10
  retries = 0
  session = requests.Session()

  while True:

    # make request and handle errors
    try:

      response_object = get_filtered_recommendations(curator, start, count, session)

    except requests.ConnectionError as ex:  # RETRY; haven't been able to test...
      if retries < MAX_RETRIES:
        logging.info("retrying...")
        logging.debug(traceback.format_exc())
        session = requests.Session()  # renew session
        sleep(5 + 15*retries)
        retries += 1
        continue
      else:
        raise RuntimeError("Max retries attempted.") from ex


    # return response as next element of generator
    yield response_object

    # check if done
    if (start + count) >= response_object['total_count']:
      break

    # prepare for next request
    start += count
    retries = 0

    # insert random delay of approx 1.0s  # doesn't seem to be needed
    #sleep(0.5 + random())

  return # end generator


def run(curator:str):

  try:

    output_filename = f"recs_{curator}_{datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')}.csv"

    with open(output_filename, "w", newline='', encoding="utf-8") as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(HEADER)

      for response_object in scrape_recommendations(curator):
        recommendation_batch = extract_recommendations(response_object["results_html"])

        for recommendation in recommendation_batch:
          writer.writerow(recommendation.values())

    logging.info("done scraping!")

  except Exception as ex:
    raise RuntimeError("Ran into a fatal error.") from ex


if __name__ == "__main__":

  # will fill this out at a later time

  # need an argument for 'curator'

  #parser = argparse.ArgumentParser()
  #args = parser.parse_args()
  #run(**args) # to_dict()??

  pass
