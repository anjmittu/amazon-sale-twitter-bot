import tweepy
import requests
from bs4 import BeautifulSoup
import os


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers',
    }

    def check_price():
        page = requests.get(os.environ.get('URL'), headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id="productTitle").get_text()
        price = soup.find(id="priceblock_ourprice").get_text()

        converted_price = float(price[1:])

        if converted_price < int(os.environ.get('ORIGINAL_PRICE')):
            tweet(title, converted_price)

    def tweet(product, price):
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET_KEY'))
        auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_SECRET_TOKEN'))

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

        # Send the tweet
        api.update_status("The price for {} has changed to ${}".format(product, price))

    check_price()


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    main({})