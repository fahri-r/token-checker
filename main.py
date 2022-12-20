import os
import requests
from datetime import datetime
from db import get_database
import validators

db = get_database()


def add_token(token_address, chain, chat_id):

    # Token Address Validation
    if chain == "bsc":
        wrapped_address = os.getenv('WBNB_ADDRESS')
        url = f"https://deep-index.moralis.io/api/v2/{token_address}/{wrapped_address}/pairAddress?chain=bsc&exchange=pancakeswapv2"
    else:
        wrapped_address = os.getenv('WETH_ADDRESS')
        url = f"https://deep-index.moralis.io/api/v2/{token_address}/{wrapped_address}/pairAddress?chain=eth&exchange=uniswapv2"

    check_pair = requests.get(
        url=url,
        headers={
            "Accept": "application/json",
            "X-API-Key": os.getenv('MORALIS_API_TOKEN'),
        }
    )

    if check_pair.status_code != 200:
        msg = f"Please input valid Token Address!"
        return msg

    # Check Token already in database or no?
    is_token_added = db.token.find_one({
        "token0Contract": token_address.lower(),
        "chain": chain.upper()
    })

    if not is_token_added:
        pair_address = check_pair.json()["pairAddress"]

        if check_pair.json()["token0"]["address"] == wrapped_address:
            name = check_pair.json()["token1"]["name"]
            symbol = check_pair.json()["token1"]["symbol"]
            address = check_pair.json()["token1"]["address"]
        else:
            name = check_pair.json()["token0"]["name"]
            symbol = check_pair.json()["token0"]["symbol"]
            address = check_pair.json()["token0"]["address"]

        if chain == "bsc":
            url = f"https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress={address}&apikey={os.getenv('BSC_API_TOKEN')}"
        else:
            url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={address}&apikey={os.getenv('ETH_API_TOKEN')}"

        total_supply = requests.get(url=url)

        token = db.token.insert_one(
            {
                "chain": chain.upper(),
                "pairAddress": pair_address,
                "token0Contract": address,
                "token0Name": name,
                "token0Symbol": symbol,
                "token0Supply": total_supply.json()["result"],
                "createdAt": datetime.now()
            })
        token_id = token.inserted_id
    else:
        token_id = is_token_added["_id"]

    # Check Group already in database or no?
    is_group_added = db.group.find_one({"chatId": chat_id, })
    if is_group_added:
        group_id = is_group_added["_id"]
    else:
        group = db.group.insert_one({
            "chatId": group_id,
            "isPremium": False,
        })
        group_id = group.inserted_id

    # Check token in spesific group already in database or no?
    is_added = db.groupToken.find_one({
        "tokenId": token_id,
        "groupId": group_id
    })
    if is_added:
        msg = f"Pair Already Added"
    else:
        db.groupToken.insert_one({
            "tokenId": token_id,
            "groupId": group_id,
            "isPaused": False,
            "emoji": "🟢",
            "emojiAmount": 2,
            "minBuy": 0.5,
            "createdAt": datetime.now(),
        })
        msg = f"Pair Added"
    return msg


def buy_check():
    tokens_id = db.groupToken.distinct("tokenId")

    # Checking every token id inside grouptoken collection
    for token_id in tokens_id:
        token = db.token.find_one({"_id": token_id})
        print(f"Checking {token['token0Symbol']}")

        query = f"""{{
            swaps(where: {{ pair: "{token['pairAddress']}" }}, orderBy: timestamp, orderDirection: desc, first:5) {{
                transaction {{
                    id
                    timestamp
                }}
            }}
            }}"""
        r = requests.post(f"https://bsc.streamingfast.io/subgraphs/name/pancakeswap/exchange-v2",
                          json={"query": query}).json()["data"]["swaps"]

        # Loop if there are transactions inside response
        for tx in r:
            hash = tx["transaction"]["id"]
            tx = db.txHistory.find_one({"hash": hash})
            if tx:
                print("Buy Already Sent")
                break

            db.txHistory.insert_one({
                "hash": hash,
                "chain": "BSC"
            })

            url = f"https://deep-index.moralis.io/api/v2/transaction/{hash}?chain=bsc"
            r = requests.get(url=url, headers={
                "Accept": "application/json",
                "X-API-Key": os.getenv('MORALIS_API_TOKEN'),
            })

            if int(r.json()["value"]) == 0:
                print("No Buy Only Sold")
                continue

            bnb_usd = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies=usd"
            ).json()["binancecoin"]["usd"]

            bnb_token = requests.get(
                f"https://deep-index.moralis.io/api/v2/erc20/{token['token0Contract']}/price?chain=bsc", headers={
                    "x-api-key": os.getenv('MORALIS_API_TOKEN')})

            if bnb_token.status_code != 200:
                bnb_token = requests.get(f"https://deep-index.moralis.io/api/v2/{token['pairAddress']}/erc20?chain=bsc", headers={
                    "x-api-key": os.getenv('MORALIS_API_TOKEN')}).json()
                decimals = bnb_token[1]["decimals"]
                bnb_balance = int(bnb_token[0]["balance"]) / \
                    pow(10, bnb_token[0]["decimals"])
                token_balance = int(bnb_token[1]["balance"]) / \
                    pow(10, decimals)
                bnb_token_price = bnb_balance / token_balance
            else:
                data = bnb_token.json()
                decimals = data["nativePrice"]["decimals"]
                bnb_token_price = int(data["nativePrice"]["value"]) / \
                    pow(10, decimals)

            spent = int(r.json()["value"]) / pow(10, 18)
            spent_usd = spent * bnb_usd
            price = bnb_token_price
            price_usd = bnb_token_price * bnb_usd
            got = round(spent / price, 3)
            got = ('{:,}'.format(got))
            supply = int(token["token0Supply"]) / \
                pow(10, decimals)
            mcap = round(price_usd * supply, 2)
            mcap = ('{:,}'.format(mcap))

            groups = db.groupToken.aggregate([
                {
                    "$match": {
                        "tokenId": token["_id"],
                        "minBuy": {"$lt": spent}
                    }
                },
                {
                    "$lookup": {
                        "from": "group",
                        "localField": "groupId",
                        "foreignField": "_id",
                        "as": "group",
                    }
                },
                {
                    "$unwind": '$group'
                },
                {
                    "$lookup": {
                        "from": "token",
                        "localField": "tokenId",
                        "foreignField": "_id",
                        "as": "token"
                    }
                },
                {
                    "$unwind": '$token'
                }
            ])

            for group in groups:
                emoji = str(group["emoji"]) + ((str(group["emoji"]) *
                                                round(int(float(spent)), 2)) * int(group["emojiAmount"]))

                message = (
                    f"<b>{token['token0Name']} Buy</b>\n"
                    f"{emoji}\n"
                    f"<b>Spent</b>: {round(spent, 11)} BNB (${round(spent_usd,11)})\n"
                    f"<b>Got</b>: {got} {token['token0Symbol']}\n"
                    f"<b>Price</b>: {round(price, 11):.11f} (${round(price_usd, 11):.11f})\n"
                    f'<b>MCap</b>: ${mcap}\n'
                    f'| <a href="https://bscscan.com/tx/{hash}">TX</a> | <a href="https://www.dextools.io/app/bsc/pair-explorer/{token["pairAddress"]}">Chart</a> | <a href="https://bscscan.com/address/{r.json()["from_address"]}">Buyer</a> | <a href="https://pancakeswap.finance/swap?outputCurrency={token["token0Contract"]}">Pancakeswap</a> |\n\n'
                )

                try:
                    print(message)
                    continue

                except Exception as e:
                    print(e)
                    continue


def change_ads(url, chat_id):
    if not validators.url(url):
        text = f"Please input valid URL!"
        return text

    db.group.update_one(
        {
            'chatId': chat_id
        },
        {'$set': {
            'adsUrl': url,
        },
        }
    )
    text = "Ads URL successfully changed"
    return text


def remove_ads(chat_id):
    db.group.update_one(
        {
            'chatId': chat_id
        },
        {'$set': {
            'adsUrl': "",
        },
        }
    )
    text = "Ads URL successfully removed"

    return text


def change_min_buy(min_buy, group_id, token_id):
    try:
        min_buy = int(min_buy)
    except:
        try:
            min_buy = float(min_buy)
        except:
            min_buy = min_buy

    if not isinstance(min_buy, (int, float)):
        msg = f"Please input valid value!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'minBuy': min_buy,
        },
        }
    )

    text = "Minimum buy successfully changed"
    return text


def change_emoji(group_id, token_id, emoji):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'emoji': emoji,
        },
        }
    )

    text = "Emoji successfully changed"
    return text


def delete_token(group_id, token_id):
    db.groupToken.delete_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
    )
    text = "Token successfully deleted"
    return text


def change_telegram(url, group_id, token_id):
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'telegramUrl': url,
        },
        }
    )

    text = "Telegram URL successfully changed"
    return text


def remove_telegram(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'telegramUrl': "",
        },
        }
    )
    text = "Telegram URL successfully removed"
    return text


def change_presale(url, group_id, token_id):
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return msg
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'presaleUrl': url,
        },
        }
    )

    text = "Presale URL successfully changed"
    return text


def remove_presale(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'presaleUrl': "",
        },
        }
    )
    text = "Presale URL successfully removed"
    return text


def change_chart(url, group_id, token_id):
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'chartUrl': url,
        },
        }
    )

    text = "Chart URL successfully changed"
    return text


def remove_chart(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'chartUrl': "",
        },
        }
    )
    text = "Chart URL successfully removed"
    return text


def change_discord(url, group_id, token_id):
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'discordUrl': url,
        },
        }
    )

    text = "Discord URL successfully changed"
    return text


def remove_discord(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'discordUrl': "",
        },
        }
    )
    text = "Discord URL successfully removed"
    return text


def change_twitter(url, group_id, token_id):
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'twitterUrl': url,
        },
        }
    )

    text = "Twitter URL successfully changed"
    return text


def remove_twitter(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'twitterUrl': "",
        },
        }
    )
    text = "Twitter URL successfully removed"
    return text


def change_website(url, group_id, token_id):
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'websiteUrl': url,
        },
        }
    )

    text = "Website URL successfully changed"
    return text


def remove_website(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'websiteUrl': "",
        },
        }
    )
    text = "Website URL successfully removed"
    return text


def change_image(url, group_id, token_id):
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'imageUrl': url,
        },
        }
    )

    text = "Image URL successfully changed"
    return text


def remove_image(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'imageUrl': "",
        },
        }
    )
    text = "Image URL successfully removed"
    return text


def change_content(text, group_id, token_id):
    if not text:
        msg = f"Please input content!"
        return msg

    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'content': text,
        },
        }
    )

    text = "Content successfully changed"
    return text


def remove_content(group_id, token_id):
    db.groupToken.update_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
        {'$set': {
            'content': "",
        },
        }
    )
    text = "Content successfully removed"
    return text


def resume_all(chat_id):
    group = db.group.find_one({
        "chatId": chat_id
    })
    db.groupToken.update_many(
        {
            'groupId': group["_id"]
        },
        {'$set': {
            'isPaused': False,
        },
        }
    )
    text = "Token buy notification successfully continued!"
    return text


def pause_all(chat_id):
    group = db.group.find_one({
        "chatId": chat_id
    })
    db.groupToken.update_many(
        {
            'groupId': group["_id"]
        },
        {'$set': {
            'isPaused': True,
        },
        }
    )
    text = "Token buy notification successfully paused!"
    return text


def delete_all(chat_id):
    group = db.group.find_one({
        "chatId": chat_id
    })
    db.groupToken.delete_many(
        {
            'groupId': group["_id"]
        }
    )
    text = "All token successfully deleted!"
    return text
