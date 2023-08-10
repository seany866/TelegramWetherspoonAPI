import requests
import json
import logging
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = 'YOUR_TOKEN'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

payload = {
    "location": {"lng": 0, "lat": 0},
    "paging": {"numberPerPage": 1000, "page": 1, "UsePagination": True},
    "term": None,
    "searchType": 0,
    "searchAddress": False
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Content-Type': 'application/json'
}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Wetherspoons pub search - Use the commands /pub {city you want to search} and /id {pub id} {brand drink} to search for pubs and drinks.')


def search_pub(update: Update, context: CallbackContext) -> None:
    city = update.message.text.split('/pub ')[-1]

    response = requests.post("https://api.jdwetherspoon.com/api/pubs", headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()

        results = [pub for pub in data['results'] if pub['city'].lower() == city.lower()]

        message = ""
        for pub in results:
            message += f"Pub Name: {pub['name']}\nAddress: {pub['address1']}, {pub['city']}, {pub['county']}, {pub['postcode']}\nTelephone: {pub['telephone']}\nPub Number: {pub['pubNumber']}\nPub ID: {pub['id']}\nURL: {pub['url']}\n---\n"

        if not message:
            message = "No pubs found in the specified city."
        
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(f"Request failed with status code: {response.status_code}")


def search_drink(update: Update, context: CallbackContext) -> None:
    input_data = update.message.text.split('/id ')[-1]
    values = input_data.split()
    
    if len(values) < 2:
        message = "Please provide the pub ID and the drink you are searching."
        update.message.reply_text(message)
        return
    
    pub_id = values[0]
    drink = ' '.join(values[1:])
    
    menu_response = requests.get(f"https://static.wsstack.nn4maws.net/content/v5/menus/{pub_id}.json")

    if menu_response.status_code == 200:
        menu_data = menu_response.json()

        drink_found = False
        if 'menus' in menu_data:
            menus = menu_data['menus']
            for menu in menus:
                if 'subMenu' in menu:
                    submenus = menu['subMenu']
                    for submenu in submenus:
                        if 'productGroups' in submenu:
                            product_groups = submenu['productGroups']
                            for group in product_groups:
                                if 'products' in group:
                                    products = group['products']
                                    for product in products:
                                        if 'eposName' in product and product['eposName'].lower() == drink.lower():
                                            # Prepare the response message
                                            message = f"Epos Name: {product['eposName']}\n"
                                            for portion in product['portions']:
                                                message += f"Portion: {portion['name']}\nPrice: £{portion['displayPrice']}\n"
                                            drink_found = True
                                            break
                                        elif 'eposName' in product and drink.lower() in product['eposName'].lower():
                                            # Prepare the response message
                                            message = f"Epos Name: {product['eposName']}\n"
                                            for portion in product['portions']:
                                                message += f"Portion: {portion['name']}\nPrice: {portion['displayPrice']}\n"
                                            drink_found = True
                                            break
                                if drink_found:
                                    break
                        if drink_found:
                            break
                if drink_found:
                    break

        if not drink_found:
            message = "Drink not found in the menu."
    else:
        message = f"Request failed with status code: {menu_response.status_code}"

    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)



def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Invalid command. Please use /pub or /id followed by the required parameters.')


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pub", search_pub))
    dispatcher.add_handler(CommandHandler("id", search_drink))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
