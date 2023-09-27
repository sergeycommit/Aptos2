from time import sleep
import random

from aptos_sdk.account import Account
from loguru import logger

from settings import *


def bridge_from_aptos(client, privat_key: str, recepient, amount: int, token_from: float) -> None:
    try:
        current_account = Account.load_key(key=privat_key)

    except ValueError:
        logger.error(f'{privat_key} | Невалидный Private Key')
        return

    while True:
        token_from = token_from.upper()
        try:
            COIN_STORE = "0x1::coin::CoinStore"
            account_balance = int(client.account_resource(current_account.address(),
                                                               f"{COIN_STORE}<{TOKEN_ADDRESSES[token_from][0]}>")[
                                      'data']['coin']['value'])

            print('Balance: ', account_balance,
                  'amount: ', amount*(10**TOKEN_ADDRESSES[TOKEN_BRIDGE][1]),
                  'address: ', current_account.address())

            if account_balance < amount:
                logger.error(f'{privat_key} | Маленький баланс: {account_balance / 10**TOKEN_ADDRESSES[token_from][1]}')
                return

            payload = {
                "function": "0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::coin_bridge::send_coin_from",
                "type_arguments": [
                        TOKEN_ADDRESSES[token_from][0]
                        ],
                 "arguments": [
                        CHAINS[TO_CHAIN],
                        "0x000000000000000000000000" + recepient[2:],
                        str(int(amount*(10**TOKEN_ADDRESSES[TOKEN_BRIDGE][1]))),
                        str(BRIDGE_GAS_PRICE+random.randint(0, 15)),
                        "0",
                        False,
                        "0x000100000000000249f0",
                        "0x"
                    ],
                 "type": "entry_function_payload"
                }

            tx_hash = client.submit_transaction(current_account, payload)
            sleep(5)
            try:
                print(client.wait_for_transaction(tx_hash))
            except Exception as error:
                logger.error(f'{privat_key} | {error}')
                return

            logger.success(f'{privat_key} | https://explorer.aptoslabs.com/txn/{tx_hash}?network=mainnet')

        except Exception as error:
            logger.error(f'{privat_key} | {error}')

            if 'INSUFFICIENT_BALANCE_FOR_TRANSACTION_FEE' in str(error):
                if account_balance:
                    logger.error(f'{privat_key} | Маленький баланс: {account_balance / 100000000}')

                else:
                    logger.error(f'{privat_key} | Маленький баланс')

                return

            elif 'SEQUENCE_NUMBER_TOO_OLD' or '"Transaction already in mempool with a different payload"' in str(error):
                sleep(1)
                continue

            elif '{"message":"' in str(error):
                return

        else:
            return