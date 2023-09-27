"""
General settings
"""
### Token name: [   token adress, token decimal ]
TOKEN_ADDRESSES = {
    'CAKE': ["0x159df6b7689437016108a019fd5bef736bac692b6d4a1f10c941f6fbb9a74ca6::oft::CakeOFT", 8],
    'BLT': ["0xfbab9fb68bd2103925317b6a540baa20087b1e7a7a4eb90badee04abb6b5a16f::blt::Blt", 8],
    'APT': ["0x1::aptos_coin::AptosCoin", 8],
    'USDT': ["0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea::coin::USDT", 6],
    'WETH': ["0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::WETH", 6],
    'USDC': ["0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDC", 6]
}

#   Массив сетей и их id для бриджа
CHAINS = {
    'optimism': "111",
    'avalanche': "106",
    'polygon': "109"
}

#   Газ лимит, газ прайс
GAS_LIMIT = 4000
GAS_PRICE = 100

#   RPC
NODE_URL = "https://rpc.ankr.com/http/aptos/v1"

# количество транзакций на кошелек
ITERATIONS = 1

# пропускать каждый N-ый кошелек без перемешивания. False если простое перемешивание
N = 2   # number or False

# Пауза между операциями на кошельках. Указано в секундах ОТ и ДО.
WAIT_FROM = 2
WAIT_TO = 5


"""
Module 0 - wallets generator
Выберите мод:
0 - достать адреса из приватников
1 - сгенерировать n кошельков
"""

MODE = 1
N = 100  # количество кошельков для генерации, только для мода 1


"""
Module 1 - binance withdraw
"""

### Для работы модуля необходимо добавить апи с бинанса в API_KEY и в API_SECRET в файле modules/binance_withdraw.py

symbolWithdraw = 'APT'
network = 'APT'  # ETH | BSC | AVAXC | MATIC | ARBITRUM | OPTIMISM | APT | CELO etc.
RANDOM_WITHDRAW = True      # True - рандомное количество из диапазона, False - фиксированное
WITHDRAW_AMOUNT_FROM = 0.02
WITHDRAW_AMOUNT_TO = 0.025


"""
Module 2 - aptos_swap
Выберите токены для свапа из TOKEN_ADDRESSES в начале страницы
"""

DEX = [     'pancake', 'liquid'     ]       # Указать через запятую Dex из которых рандомно выбрать: pancake, liquid
TOKEN_FROM = [  'APT'   ]       # укажите через запятую несколько монет для рандома
TOKEN_TO = [    'USDC'  ]
RANDOM_SWAP = True   # True - рандомное количество из диапазона, False - фиксированное
SWAP_AMOUNT_FROM = 0.0001
SWAP_AMOUNT_TO = 0.0001
SLIPPAGE = 0.5


"""
Module 3 - aptos_bridge
Выберите токены для бриджа изависит от сетей
"""

BRIDGE_GAS_PRICE = 6500000
TOKEN_BRIDGE = 'USDC'
BRIDGE_RANDOM = True   # True - рандомное количество из диапазона, False - фиксированное
BRIDGE_AMOUNT_FROM = 0.00001
BRIDGE_AMOUNT_TO = 0.00002
TO_CHAIN = 'polygon'
BRIDGE_SLIPPAGE = 3


"""
Module 4 - add_liquidity
Выберите токены для бриджа изависит от сетей
"""

DEX_LIQUIDITY = [     'liquid'    ]       # Указать через запятую Dex из которых рандомно выбрать: pancake, liquid
#  на liquidswape не все пары пула создаются, надо смотреть. Работает USDC-APT
TOKEN_1 = 'USDC'
TOKEN_2 = 'APT'
RANDOM_LIQUIDITY = False   # True - рандомное количество из диапазона, False - фиксированное
AMOUNT_LIQUIDITY_FROM = 0.000003
AMOUNT_LIQUIDITY_TO = 0.000006
SLIPPAGE_LIQUIDITY = 3


"""
Module 5 - create NFT and listing

Создает NFT коллекцию с рандомным именем, описанием и картинкой и листит на Topaz
"""

# Список PREFIX и NAMES из которых рандомно будет добавлено к имени NFT и коллекции помимо рандома городов.
# Измени эти списки, вставь свои слова для рандома
PREFIX = [   "Aptos", "Web3", "Technology", "AI", "NFT", "Gold", "Silver", "Diamond", "Platina", "Crypto"   ]
NAMES = [   "August", "2023", "August_2023", "CocoJambo", "Tech"  ]
LISTING = True
RANDOM_NFT_PRICE = True
NFT_PRICE_FROM = 0.001       # подставьте значения цены НФТ для рандома
NFT_PRICE_TO = 0.001


"""
Module 6 - randome module 2(swap) or 4(add_liquidity)

Запускает рандомный модуль 2 свап или 4 добавление ликвидности с рандомными DEX
"""

# Настройте модули 2 и 4
