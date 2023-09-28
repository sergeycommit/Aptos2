import time
from time import sleep
import random

from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from loguru import logger

from settings import *
from modules.binance_withdraw import binance_withdraw
from modules.swap import swap_cake
from modules.add_liquidity import add_liquidity
from modules.aptos_bridge import bridge_from_aptos
from modules.create_nft import create_nft


def write_unused_keys():
    with open(file_name, 'a') as f:
        for key in (set(private_keys) - set(used_keys)):
            f.write(key + '\n')

def generate_wallets(wallets):
    if isinstance(wallets, int):
        with open(f'new_aptos_private_keys{time.time()}.txt', 'a+') as f:
            for i in range(wallets):
                f.write(str(Account.generate().private_key) + '\n')

    else:
        with open(f'aptos_addresses{time.time()}.txt', 'a+') as f:
            for key in wallets:
                f.write(str(Account.load_key(key=key).address()) + '\n')

if __name__ == '__main__':
    print(f'----------------------------------------------------'
          f'\nsubscribe to us : https://t.me/my_utils\n'
          f'----------------------------------------------------')

    MODULE = int(input('''
    MODULE:
    0.  generate_aptos_wallets
    1.  binance_withdraw
    2.  aptos_swap
    3.  aptos_bridge
    4.  add_liquidity
    5.  create_nft_and_listing
    6. random module(swap or add_liquidity)
    Выберите модуль (0 - 6) : '''))

    with open('private_keys.txt', 'r', encoding='utf-8-sig') as file:
            private_keys = [row.strip() for row in file]

    file_name = 'unused_keys' + str(int(time.time()))
    with open(file_name, 'w') as f:
        f.write('')

    used_keys = []

    class ClientConfig:
        """Common configuration for clients, particularly for submitting transactions"""

        expiration_ttl: int = 600
        gas_unit_price: int = GAS_PRICE
        max_gas_amount: int = GAS_LIMIT
        transaction_wait_in_seconds: int = 20


    REST_CLIENT = RestClient(NODE_URL, client_config=ClientConfig)

    if MODULE == 0:
        if MODE:
            generate_wallets(int(N))
        else:
            generate_wallets(private_keys)
        exit()

    if MODULE in (2, 4, 6):
        logger.info(f'Успешно загружено {len(private_keys)} wallet\'s')
        if not MISS_NUM:
            random.shuffle(private_keys)
        for n in range(ITERATIONS):
            for num, key in enumerate(private_keys):
                if not MISS_NUM:
                    pass
                elif (num+1)%MISS_NUM == 0:
                    continue
                if MODULE == 2:
                    if RANDOM_SWAP:
                        amount = random.uniform(SWAP_AMOUNT_FROM, SWAP_AMOUNT_TO)
                    else:
                        amount = SWAP_AMOUNT_FROM
                    swap_cake(REST_CLIENT, key, random.choice(DEX), amount, SLIPPAGE, random.choice(TOKEN_FROM),
                              random.choice(TOKEN_TO))
                elif MODULE == 4:
                    if RANDOM_LIQUIDITY:
                        amount = random.uniform(AMOUNT_LIQUIDITY_FROM, AMOUNT_LIQUIDITY_TO)
                    else:
                        amount = AMOUNT_LIQUIDITY_FROM
                    add_liquidity(REST_CLIENT, key, random.choice(DEX_LIQUIDITY), amount, SLIPPAGE_LIQUIDITY,
                                  TOKEN_1, TOKEN_2)
                elif MODULE == 6:
                    choose = random.choice((0,1))
                    if choose:
                        if RANDOM_LIQUIDITY:
                            amount = random.uniform(AMOUNT_LIQUIDITY_FROM, AMOUNT_LIQUIDITY_TO)
                        else:
                            amount = AMOUNT_LIQUIDITY_FROM
                        add_liquidity(REST_CLIENT, key, random.choice(DEX_LIQUIDITY), amount, SLIPPAGE_LIQUIDITY,
                                      TOKEN_1, TOKEN_2)
                    else:
                        if RANDOM_SWAP:
                            amount = random.uniform(SWAP_AMOUNT_FROM, SWAP_AMOUNT_TO)
                        else:
                            amount = SWAP_AMOUNT_FROM
                        swap_cake(REST_CLIENT, key, random.choice(DEX), amount, SLIPPAGE, random.choice(TOKEN_FROM),
                                  random.choice(TOKEN_TO))
                time.sleep(random.randint(WAIT_FROM, WAIT_TO))
                used_keys.append(key)

            write_unused_keys()

    if MODULE == 3:
        with open('recepient_addresses.txt', 'r', encoding='utf-8-sig') as file:
            recepients = [row.strip() for row in file]

        wallets_dict, wallets = {}, {}
        for wallet_num in range(len(private_keys)):
            wallets_dict[private_keys[wallet_num]] = recepients[wallet_num]

        keys = list(wallets_dict.keys())
        random.shuffle(keys)
        for key in keys:
            wallets[key] = wallets_dict[key]

        assert len(private_keys) == len(wallets), \
            'Количество кошельков отправителей и получателей не равно. Проверьте также пробелы в конце фалов'
        logger.info(f'Успешно загружено {len(private_keys)} wallet\'s')

        for n in range(ITERATIONS):
            for from_wallet, to_wallet in wallets.items():
                if BRIDGE_RANDOM:
                    amount = random.uniform(BRIDGE_AMOUNT_FROM, BRIDGE_AMOUNT_TO)
                else:
                    amount = BRIDGE_AMOUNT_FROM
                bridge_from_aptos(REST_CLIENT, from_wallet, to_wallet, amount, TOKEN_BRIDGE)
                time.sleep(random.randint(WAIT_FROM, WAIT_TO))

                used_keys.append(from_wallet)

        write_unused_keys()

    if MODULE == 1:
        with open('withdraw_addresses', 'r', encoding='utf-8-sig') as f:
            addresses = [row.strip() for row in f]
        logger.info(f'Успешно загружено {len(addresses)} wallet\'s')
        random.shuffle(addresses)
        for address in addresses:
            if RANDOM_WITHDRAW:
                amount = round(random.uniform(WITHDRAW_AMOUNT_FROM, WITHDRAW_AMOUNT_TO), 5)
            else:
                amount = WITHDRAW_AMOUNT_FROM
            binance_withdraw(address, amount, symbolWithdraw, network)
            time.sleep(random.randint(WAIT_FROM, WAIT_TO))

    if MODULE == 5:
        logger.info(f'Успешно загружено {len(private_keys)} wallet\'s')

        if not MISS_NUM:
            random.shuffle(private_keys)

        for n in range(ITERATIONS):

            for num, key in enumerate(private_keys):

                if not MISS_NUM:
                    pass
                elif (num + 1) % MISS_NUM == 0:
                    continue

                if RANDOM_NFT_PRICE:
                    NFT_PRICE_FROM = random.uniform(NFT_PRICE_FROM, NFT_PRICE_TO)
                create_nft(REST_CLIENT, key, random.choice(PREFIX), random.choice(NAMES), LISTING, NFT_PRICE_FROM)
                time.sleep(random.randint(WAIT_FROM, WAIT_TO))

                used_keys.append(key)

        write_unused_keys()

    logger.info('DONE')
