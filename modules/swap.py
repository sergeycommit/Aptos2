import json
import random
import time
from time import sleep

import requests
from aptos_sdk.account import Account
from aptos_sdk.transactions import TransactionArgument, TransactionPayload, TypeTag, EntryFunction, Serializer, \
    StructTag, RawTransaction, SignedTransaction
from aptos_sdk.authenticator import Authenticator, Ed25519Authenticator
from loguru import logger

from settings import *

ROUTERS = {
        'pancake':  "0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::router::swap_exact_input",
        'liquid':   "0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::scripts_v2::swap",
        'thala':    "0x89576037b3cc0b89645ea393a47787bb348272c76d6941c574b053672b848039::aggregator::swap"
}

def get_price(token_from, token_to):
    response = requests.get(
        f'https://min-api.cryptocompare.com/data/price?fsym={token_from}&tsyms={token_to}').text

    return json.loads(response)[token_to]

def swap_cake(client, privat_key: str, dex, amount: int, slippage: int, token_from: float, token_to: float) -> None:
        try:
            current_account = Account.load_key(key=privat_key)

        except ValueError:
            logger.error(f'{privat_key} | Невалидный Private Key')
            return

        token_from, token_to = token_from.upper(), token_to.upper()
        ROUTER = ROUTERS[dex]
        try:
            COIN_STORE = "0x1::coin::CoinStore"

            account_balance = int(client.account_resource(current_account.address(),
                                                          f"{COIN_STORE}<{TOKEN_ADDRESSES[token_from][0]}>")['data'][
                                      'coin']['value'])

            amount_to = amount * get_price(token_from, token_to) * (1 - slippage / 100)

            print('Balance: ', account_balance,
                  'amount: ', amount,
                  'amout_to', amount_to)

            if account_balance < amount:
                logger.error(f'{privat_key} | Маленький баланс: '
                             f'{account_balance / 10 ** TOKEN_ADDRESSES[token_from][1]}')
                return

            transaction_arguments = [
                TransactionArgument(int(amount * (10 ** TOKEN_ADDRESSES[token_from][1])), Serializer.u64),
                TransactionArgument(int(amount_to * (10 ** TOKEN_ADDRESSES[token_to][1])), Serializer.u64),
            ]

            if 'liquid' in dex:
                ARGS = [TypeTag(StructTag.from_str(TOKEN_ADDRESSES[token_from][0])),
                        TypeTag(StructTag.from_str(TOKEN_ADDRESSES[token_to][0])),
                        TypeTag(StructTag.from_str(
                            "0x190d44266241744264b964a37b8f09863167a12d3e70cda39376cfb4e3561e12::curves::Uncorrelated"))]

            elif dex == 'pancake':
                ARGS = [TypeTag(StructTag.from_str(TOKEN_ADDRESSES[token_from][0])),
                        TypeTag(StructTag.from_str(TOKEN_ADDRESSES[token_to][0]))]

            elif dex == 'thala':
                ARGS = [TypeTag(StructTag.from_str(TOKEN_ADDRESSES[token_from][0])),
                        TypeTag(StructTag.from_str(TOKEN_ADDRESSES[token_to][0]))]

            payload = EntryFunction.natural(
                ROUTER,
                ROUTER.split('::')[-1],
                ARGS,
                transaction_arguments,
            )

            raw_transaction = RawTransaction(
                current_account.address(),
                client.account_sequence_number(current_account.address()),
                TransactionPayload(payload),
                int(GAS_LIMIT * (random.uniform(1, 1.11))),
                GAS_PRICE,
                int(time.time()) + 600,
                chain_id=1,
            )
            signature = current_account.sign(raw_transaction.keyed())
            authenticator = Authenticator(
                Ed25519Authenticator(current_account.public_key(), signature)
            )

            tx_hash = client.submit_bcs_transaction(SignedTransaction(raw_transaction, authenticator))
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
                    logger.error(f'{privat_key} | Непрошла транза маленький баланс:'
                                 f' {account_balance / 10 ** TOKEN_ADDRESSES[token_from][1]}')

                else:
                    logger.error(f'{privat_key} | Маленький баланс')

                return

            elif '{"message":"' in str(error):
                return

        else:
            return