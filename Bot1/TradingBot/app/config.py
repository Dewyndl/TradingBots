import json
from pathlib import Path

bot_token = "8110699202:AAF0UOwOGC2E64x4eiMs8kdf3RHHbV-IT80"
api_key = "1d4d07d2-2f92-4cc8-9876-ed42588e953d"
api_secret_key = "F77F357DE09F018D098FC84B4C3E4B3E"
passphrase = "Shdbxh26!)"
proxies = "http://user218539:okl7c6@31.6.53.197:3460"

private_database = 'TradingBot/private.db'
path_to_common_bots = Path(__file__).parent.parent.parent.parent
public_database = path_to_common_bots / "public_database.db"
public_config = path_to_common_bots / "public_config.json"

with open(public_config, 'r', encoding='utf-8') as f:
    data = json.load(f)  # data — это уже словарь (dict)

user_list = data["user_list"]
proxies_list = data["proxies"]

