#!/usr/bin/python
""" the bot package servers as a telegram adapter """
import time
import telegram
import emoji
import config as cfg

TELLIE = telegram.Bot(token=cfg.telegram_token)

TEST_CHANNELS = [
    cfg.telegram_chat_dev
]

PROD_CHANNELS = [cfg.telegram_chat_prod]


def delivery_boy(text, channels):
    """ sends a message to an array of channels"""
    for channel in channels:
        TELLIE.send_message(chat_id=channel, text=text,
                            parse_mode="Markdown", disable_web_page_preview=True)


def build_info_template():
    moon_symbol = emoji.emojize(":full_moon:")
    crystal_ball_symbol = emoji.emojize(":crystal_ball:")

    text = moon_symbol + " Moon Room Resources " + moon_symbol + "\n"
    text += "- *FREE* Trading Guide -> bit.ly/2vFCM5W \n"
    text += "- Roadmap -> bit.ly/2wOPi7Z \n"
    text += "- Website -> bit.ly/2wmfMLz\n"
    text += "- Report bugs! -> goo.gl/forms/CPOCGE86TwDrf1sr1\n"
    text += "- Request features! -> goo.gl/forms/bdHcPk5TsRH5roZL2\n\n"
    text += crystal_ball_symbol + \
        " Write @AustinWitherow at any time. " + \
        crystal_ball_symbol

    return text


def build_cmc_new_coins_template(new_coins):
    moon_symbol = emoji.emojize(":full_moon:")
    text = moon_symbol + " New CMC Listings! " + moon_symbol + "\n"
    count = 1

    for coin in new_coins:
        symbol = coin["symbol"]

        text += count + ". " + "[" + symbol + \
            "](coinmarketcap.com/currencies/" + symbol + ")"

        count += 1

    if cfg.env == "test":
        delivery_boy(text, TEST_CHANNELS)
        return

    delivery_boy(text, PROD_CHANNELS)


def generate_and_post_message(hourly, daily):
    """
        generates and posts a message using the build template and send message functions
        accepts hourly, daily scores
        - scores currently are expected to be of shape [{ symbol: string, score: int }]
        - scores will evolve to coins array => [{ symbol: string, scores: { medium: int }}]
        -- medium being "twitter", "reddit", "google", etc.
    """

    text = build_rating_template(hourly, "Hourly Twitter Hype") + "\n"

    if daily:
        daily_text = build_rating_template(daily, "Daily Twitter Hype")
        text += daily_text + "\n"

    text += "\nAnalyse and Trade like a PRO with [TradingView Pro](https://tradingview.go2cloud.org/aff_c?offer_id=2&aff_id=5238) today!"

    send_message(text=text)


def send_new_coin_notification(symbol):
    """ lets developers know there is a new coin that needs to get some infos """

    text = "New coin " + symbol + " needs infos!"
    delivery_boy(text, TEST_CHANNELS)


def send_message(text, category="data"):
    """ send_message sends a text message to the environment variable chat id, in markdown """

    if cfg.env == "test":
        delivery_boy(text, TEST_CHANNELS)
        return

    now = time.localtime(time.time())

    if cfg.env == "prod":
        if category == "data":

            delivery_boy(text, PROD_CHANNELS)

        if category == "info":
            delivery_boy(text, PROD_CHANNELS)


def build_rating_template(scores, title):
    """ build_rating_template builds and returns a text message for twitter based coin score ratings """

    message = emoji.emojize("*:bird:" + title + ":bird: *\n")
    for market in scores:
        symbol = market["symbol"]

        # TODO: sentiment analysis
        # - ensure length is minus one to account for negative symbol
        # - if negative use skulls.
        birds = len(str(market["score"]))
        lit_meter = ""

        for _ in range(birds):
            lit_meter += emoji.emojize(":bird:")

        message += "- [$" + symbol + \
            "](https://twitter.com/search?f=tweets&vertical=default&q=%24" + \
            symbol + ") Score => " + lit_meter

        if "name" in market:
            message += " ::: [Research](https://coinmarketcap.com/currencies/" + \
                market["name"] + ")"

        message += " | [Analyze](https://www.tradingview.com/chart/?symbol=BITTREX:" + \
            market["symbol"] + "BTC)"

        message += " | [Trade](https://bittrex.com/Market/Index?MarketName=BTC-" + \
            market["symbol"] + ")"

        message += "\n"

    return message
