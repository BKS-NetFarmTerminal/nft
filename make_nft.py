from mint_nft import mint_nft
from ton_transfer import massage_and_gift

from dotenv import load_dotenv
import os

load_dotenv()

import aiohttp

async def fetch_data(nft_type):
    async with aiohttp.ClientSession() as session:
        async with session.get(os.getenv("IMG_GEN_API")+nft_type) as response:
            if response.status == 200:
                data = await response.json()
                img_url = data["url"]
                name = data["name"]
                res = [img_url, name]
                return res
            else:
                print("ошибка:", response.status)


async def make_nft_please(nft_type, user_address):

    [img, characteristic] = await fetch_data(nft_type)
    print(characteristic)
    print(img)
    is_testnet = os.getenv("IS_TESTNET") == "True"

    nft_address = await mint_nft(characteristic, nft_type, img, is_testnet, user_address)
    result = await massage_and_gift(user_address, characteristic, nft_type, is_testnet, nft_address)
    print(nft_address)
    print(result)
    
    if is_testnet:
        link_to_nft = f'https://testnet.tonviewer.com/{nft_address}'
    else:
        link_to_nft = f'https://tonviewer.com/{nft_address}'
    return [link_to_nft, img, f"{characteristic} {nft_type}"]