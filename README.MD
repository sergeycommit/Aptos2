# Автор
https://t.me/just_commit
Канал с новостями: https://t.me/my_utils
Донаты: EVM 0xe63F5DF79667BfAa7fE002382299d1a4F0a94AEE
binance id: 28071835

# Bridge на theaptosbridge в сеть Optimism и swap в сети APTOS на pancakeswap.finance


# Запуск

Вам понадобиться установленный Python 3.10

1. перед запуском добавьте приватные ключи в private_keys.txt
2. Установка и запуск: 

Linux/Mac
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```
Windows(рекомендую) - https://www.youtube.com/watch?v=w8JEc644K7o
Windows - https://www.youtube.com/watch?v=EqC42mnbByc
```
pip install virtualenv
virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python main.py      # это команда запуска скрипта
```

# Настройки

settings.py - настройки

private_keys.txt - Aptos приватные ключи

recepient_addresses.txt - адреса EVM кошельков получателей  для бриджа

withdraw_addresses - адреса для вывода с бинанса

