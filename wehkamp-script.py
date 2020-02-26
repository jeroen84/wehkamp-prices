"""
A webscrape script that monitors the prices of articles
and notifies in case of sale for the webstore
Wehkamp (https://www.wehkamp.nl)
"""

from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import time
import logging as LOG
from pushover import Client  # for notifications
import secrets  # for Pushover API credentials

LOG.basicConfig(format='%(asctime)s %(message)s',
                filename="wehkamp.log",
                level=LOG.INFO)

website = secrets.article_url

browser_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 "
                  "Safari/537.36"}

# define number of seconds for each refresh
refreshfreq = secrets.refreshfreq

# placeholder for debugging
_DEBUG = False


def _getPricingFields(url,
                      headers):
    try:
        _response = requests.get(url, headers=headers)

        # check if the response is ok
        if _response.ok:
            LOG.info("Successful connection to %s" % url)
            _soup = BeautifulSoup(_response.text, "html.parser")

            _html_parse = []
            _html_parse.append(_soup.title.text)

            # find the specific class where price is mentioned
            _pricing_tag = _soup.find(name="div",
                                      attrs={"class":
                                             "PricingInfo__ba-pricing___3JnR4 "
                                             "flex flex-wrap "
                                             "align-right font-size-regular "
                                             "font-weight-light "
                                             "margin-bottom-xsmall"})

            if _pricing_tag is not None:
                _html_parse += list(_pricing_tag.strings)
                # return all value fields as a list
                return _html_parse
            else:
                # cannot get the pricing tag of the site
                LOG.error("Cannot fetch pricing tag of %s. "
                          "Please reconfigure." % url)
                return []
        else:  # the response is not ok
            return []
    except ConnectionError:
        LOG.error("URL is not accessible: %s" % url)
        return []
    except Exception as e:
        LOG.error("An error occured:\n\n%s" % str(e))
        return []


client = Client(secrets.pushover_userkey,
                api_token=secrets.pushover_apikey)

# the logic is = if size of the list is greater
# than 2, then the item is for sale
# in case the item is for sale, send a notification
# via Pushover

while True:
    price_fields = _getPricingFields(website,
                                     browser_header)
    LOG.info("price_fields return: %s" % str(price_fields))
    LOG.info("number of price_fields: %i" % len(price_fields))

    # if there is no sale, remain in the loop
    if len(price_fields) <= 2:
        if len(price_fields) == 0:
            client.send_message("No result from url %s.\n"
                                "Please check logging"
                                % website,
                                title="Error")
        # the price of the article is not for sale.
        elif len(price_fields) == 2:
            # if _DEBUG mode is on, send notifications
            # even when the article is not for sale
            if _DEBUG:
                client.send_message("No sale of item %s\nPrice remains %s" %
                                    (price_fields[0],
                                        str(price_fields[1])),
                                    title="No sale")
        # should not happen... but still good to notify
        else:
            client.send_message("Price fields return weird number of "
                                "elements. Please check logging",
                                title="Weird error")

        time.sleep(refreshfreq)
        continue
    else:
        client.send_message("Item %s is for sale!\nFrom %s to %s \nPlease go"
                            "to %s !" %
                            (price_fields[0],
                             str(price_fields[1]),
                             str(price_fields[2]),
                             website),
                            title="For sale!")
    break
