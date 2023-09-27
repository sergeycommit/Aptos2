import random
import json
import requests
import time

import geonamescache
from text_generation import InferenceAPIClient
from aptos_sdk.account import Account
from loguru import logger

ROUTER = "0x2c7bccf7b31baf770fdbcc768d9e9cb3d87805e255355df5db32ac9a669010a2::marketplace_v2::list"

def get_city():
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()
    city_nums = list(cities.keys())

    return cities[random.choice(city_nums)]['name']

def generate_text(prefix, city, name):
    token = "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"

    try:
        text_client = InferenceAPIClient('google/flan-t5-xxl', token)
        name = f"Make a description of {prefix} {city} {name}"
        text = text_client.generate(name).generated_text
    except:
        text = 'some describtion'

    return text


def create_nft(client, priv_key, prefix, name, listing, nft_price):
    current_account = Account.load_key(key=priv_key)
    wallet_address = current_account.address()

    city = get_city()
    collection_name = f"{prefix} {city} {name}"
    descr = generate_text(prefix, city, name)
    nft_name = "NFT " + collection_name
    nft_descr = generate_text('Token', city, name)
    img_url = get_img_url()
    supply = 10*random.randint(1, 500)
    royalty = random.randint(0, 10)

    for i in range(15):
        try:
            txn_hash = client.create_collection(
                current_account,
                collection_name,
                descr,
                f"https://{collection_name}.dev"
            )
            break
        except:
            time.sleep(1)
            continue
    if not txn_hash:
        return print(f"Сделали 15 попыток но транза не прошла на приватнике {priv_key}")

    time.sleep(5)
    try:
        client.wait_for_transaction(txn_hash)
    except Exception as error:
        logger.error(f'{priv_key} | {error}')
        return

    for i in range(15):
        try:
            txn_hash = client.create_token(
                current_account,
                collection_name,
                nft_name,
                nft_descr,
                supply,
                img_url,
                royalty,
            )
            break
        except:
            time.sleep(1)
            continue
    if not txn_hash:
        return print(f"Сделали 5 попыток но транза не прошла на приватнике {priv_key}")

    time.sleep(5)
    try:
        client.wait_for_transaction(txn_hash)
    except Exception as error:
        logger.error(f'{priv_key} | {error}')
        return

    for i in range(15):
        try:
            txn_hash = client.offer_token(
                current_account,
                wallet_address,
                wallet_address,
                collection_name,
                nft_name,
                0,
                1,
            )
            break
        except:
            time.sleep(1)
            continue
    if not txn_hash:
        return print(f"Сделали 5 попыток но транза не прошла на приватнике {priv_key}")

    time.sleep(5)
    try:
        client.wait_for_transaction(txn_hash)
    except Exception as error:
        logger.error(f'{priv_key} | {error}')
        return

    for i in range(15):
        try:
            txn_hash = client.claim_token(
                current_account,
                wallet_address,
                wallet_address,
                collection_name,
                nft_name,
                0,
            )
            break
        except:
            time.sleep(1)
            continue
    if not txn_hash:
        return print(f"Сделали 15 попыток но транза не прошла на приватнике {priv_key}")

    print("NFT created https://aptoscan.com/version/" + txn_hash)
    time.sleep(5)

    if listing:
        payload = {
            "function": ROUTER,
            "type_arguments": ["0x1::aptos_coin::AptosCoin"],
            "arguments": [
                str(int(nft_price*1000000)),
                "1",
                str(wallet_address),
                collection_name,
                nft_name,
                "0"
            ],
            "type": "entry_function_payload"
        }

        tx_hash = client.submit_transaction(current_account, payload)
        time.sleep(5)
        try:
            client.wait_for_transaction(tx_hash)
        except Exception as error:
            logger.error(f'{priv_key} | {error}')
            return

        logger.success(f'{priv_key} | NFT listed https://explorer.aptoslabs.com/txn/{tx_hash}?network=mainnet')


def get_img_url():

    for i in range(1000):
        url_nums = [5768, 6699, 7796, 7837, 7976, 6228, 6229, 10319, 10266, 8042, 8146, 7115, 5341, 9332, 6979]
        url_num = random.choice(url_nums)

        url = f'https://cdn-icons-png.flaticon.com/128/{url_num}/{url_num}{random.randint(100, 1000)}.png'

        if requests.get(url).status_code == 200:
            return url

    print("Проверил 1000 картинок ни 1 не доступна")
