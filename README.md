# Wehkamp price watcher

Wehkamp is one of the largest online retailers of the Netherlands.

This repository represents a script that watches the price of an article
at the site of Wehkamp (https://www.wehkamp.nl)

The script distinguishes normal prices from sale prices. In case the article
is on sale, a notification is sent via Pushover.

# Prequisitions
* Python 3.7.6
* BeautifulSoup 4.8.2
* Python-pushover 0.4
* Create a secrets.py file with the following variables:
  * ``article_url``: the URL of the article at Wehkamp
  * ``pushover_userkey``: your user key of Pushover
  * ``pushover_apikey``: your API key of Pushover
  * ``refreshfreq``: the refresh frequency of the website scrap, in seconds
  * Please view the ``secrets_example.py`` for an example file.


# Docker
I have included a Dockerfile which can be used to run the scrint in a Docker environment.

Follow these steps to have the Docker environment running:
* ``docker build -t wehkamp-bedbank .``
* ``docker run -d wehkamp-bedbank``

