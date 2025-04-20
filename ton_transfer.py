from tonutils.client import LiteserverClient
from tonutils.wallet import WalletV4R2

from dotenv import load_dotenv
import os

load_dotenv()

async def massage_and_gift(destination_address, characteristic, nft_type, is_testnet, nft_address):
    if is_testnet:
        link_to_nft = f'"https://testnet.tonviewer.com/{nft_address}"'
    else:
        link_to_nft = f'"https://tonviewer.com/{nft_address}"'
    comment = f"Here is your {characteristic} {nft_type}: {link_to_nft} And some money as a gift! With respect, your Network Farm Terminal"

    client = LiteserverClient(is_testnet=is_testnet)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, os.getenv('MNEMONIC_SENDER').split())

    tx_hash = await wallet.transfer(
        destination=destination_address,
        amount=0.1,
        body=comment,
    )

    print(f"Message and some money successfully delivered!")
    print(f"Transaction hash: {tx_hash}")
    return "success"