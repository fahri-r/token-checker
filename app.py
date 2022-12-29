from blacksheep import Application, FromJSON, status_code
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
import os
from datetime import datetime
import requests
from db import get_database
import validators
from operator import itemgetter
from bson.objectid import ObjectId
from docs import token

app = Application()
db = get_database()

docs = OpenAPIHandler(info=Info(title="Token Checker API", version="0.0.1"))
docs.bind_app(app)


@docs(token.create_token)
@app.router.post("/token")
async def add_token(input: FromJSON[dict]):
    token_address, chain, chat_id = itemgetter(
        'token_address', 'chain', 'chat_id')(input.value)
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
        return status_code(422, message={'message': msg})

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
        return status_code(400, message={'message': msg})
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
        return status_code(200, message={'message': msg})


@docs(token.update_tokens)
@app.router.put("/token")
async def update_tokens(input: FromJSON[dict]):
    group_id, is_paused = itemgetter(
        'group_id', 'is_paused')(input.value)

    db.groupToken.update_many(
        {
            'groupId': ObjectId(group_id),
        },
        {'$set': {
            'isPaused': True,
        },
        }
    )
    msg = "Token buy notification successfully paused!" if is_paused else "Token buy notification successfully continued!"
    return status_code(200, message={'message': msg})


@docs(token.update_token)
@app.router.put("/token/{token_id}")
async def update_token(token_id, input: FromJSON[dict]):
    group_id, is_paused = itemgetter(
        'group_id', 'is_paused')(input.value)

    db.groupToken.update_one(
        {
            'groupId': ObjectId(group_id),
            'tokenId': ObjectId(token_id)
        },
        {'$set': {
            'isPaused': is_paused,
        },
        }
    )
    msg = "Token buy notification successfully paused!" if is_paused else "All token successfully deleted!"
    return status_code(200, message={'message': msg})


@docs(token.delete_token)
@app.router.delete("/token/{token_id}")
async def delete_token(token_id, input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
    db.groupToken.delete_one(
        {
            'groupId': group_id,
            'tokenId': token_id
        },
    )
    msg = "Token successfully deleted!"
    return status_code(200, message={'message': msg})


@docs(token.delete_tokens)
@app.router.delete("/token")
async def delete_tokens(input: FromJSON[dict]):
    group_id = itemgetter(
        'group_id')(input.value)

    db.groupToken.delete_many(
        {
            'groupId': ObjectId(group_id)
        }
    )
    msg = "All token successfully deleted!"
    return status_code(200, message={'message': msg})


@docs(token.change_ads)
@app.router.put("/ads")
async def change_ads(input: FromJSON[dict]):
    url, chat_id = itemgetter('url', 'chat_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

    db.group.update_one(
        {
            'chatId': chat_id
        },
        {'$set': {
            'adsUrl': url,
        },
        }
    )
    msg = "Ads URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_ads)
@app.router.delete("/ads")
async def remove_ads(input: FromJSON[dict]):
    chat_id = itemgetter('chat_id')(input.value)
    db.group.update_one(
        {
            'chatId': chat_id
        },
        {'$set': {
            'adsUrl': "",
        },
        }
    )
    msg = "Ads URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_min_buy)
@app.router.put("/min-buy")
async def change_min_buy(input: FromJSON[dict]):
    min_buy, group_id, token_id = itemgetter(
        'min_buy', 'group_id', 'token_id')(input.value)
    try:
        min_buy = int(min_buy)
    except:
        try:
            min_buy = float(min_buy)
        except:
            min_buy = min_buy

    if not isinstance(min_buy, (int, float)):
        msg = f"Please input valid value!"
        return status_code(422, message={'message': msg})

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

    msg = "Minimum buy successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.update_emoji)
@app.router.put("/emoji")
async def change_emoji(input: FromJSON[dict]):
    group_id, token_id, emoji = itemgetter(
        'group_id', 'token_id', 'emoji')(input.value)
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

    msg = "Emoji successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.update_telegram)
@app.router.put("/telegram")
async def change_telegram(input: FromJSON[dict]):
    url, group_id, token_id = itemgetter(
        'url', 'group_id', 'token_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

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

    msg = "Telegram URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_telegram)
@app.router.delete("/telegram")
async def remove_telegram(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Telegram URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_presale)
@app.router.put("/presale")
async def change_presale(input: FromJSON[dict]):
    url, group_id, token_id = itemgetter(
        'url', 'group_id', 'token_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

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

    msg = "Presale URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_presale)
@app.router.delete("/presale")
async def remove_presale(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Presale URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_chart)
@app.router.put("/chart")
async def change_chart(input: FromJSON[dict]):
    url, group_id, token_id = itemgetter(
        'url', 'group_id', 'token_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

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

    msg = "Chart URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_chart)
@app.router.delete("/chart")
async def remove_chart(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Chart URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_discord)
@app.router.put("/discord")
async def change_discord(input: FromJSON[dict]):
    url, group_id, token_id = itemgetter(
        'url', 'group_id', 'token_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

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

    msg = "Discord URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_discord)
@app.router.delete("/discord")
async def remove_discord(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Discord URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_twitter)
@app.router.put("/twitter")
async def change_twitter(input: FromJSON[dict]):
    url, group_id, token_id = itemgetter(
        'url', 'group_id', 'token_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

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

    msg = "Twitter URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_twitter)
@app.router.delete("/twitter")
async def remove_twitter(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Twitter URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_website)
@app.router.put("/website")
async def change_website(input: FromJSON[dict]):
    url, group_id, token_id = itemgetter(
        'url', 'group_id', 'token_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

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

    msg = "Website URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_website)
@app.router.delete("/website")
async def remove_website(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Website URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_image)
@app.router.put("/image")
async def change_image(input: FromJSON[dict]):
    url, group_id, token_id = itemgetter(
        'url', 'group_id', 'token_id')(input.value)
    if not validators.url(url):
        msg = f"Please input valid URL!"
        return status_code(422, message={'message': msg})

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

    msg = "Image URL successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_image)
@app.router.delete("/image")
async def remove_image(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Image URL successfully removed"
    return status_code(200, message={'message': msg})


@docs(token.update_content)
@app.router.put("/content")
async def change_content(input: FromJSON[dict]):
    text, group_id, token_id = itemgetter(
        'text', 'group_id', 'token_id')(input.value)
    if not text:
        msg = f"Please input content!"
        return status_code(422, message={'message': msg})

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

    msg = "Content successfully changed"
    return status_code(200, message={'message': msg})


@docs(token.delete_content)
@app.router.delete("/content")
async def remove_content(input: FromJSON[dict]):
    group_id, token_id = itemgetter(
        'group_id', 'token_id')(input.value)
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
    msg = "Content successfully removed"
    return status_code(200, message={'message': msg})
