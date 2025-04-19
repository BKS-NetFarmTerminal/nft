from tonutils.client import LiteserverClient
from tonutils.wallet import WalletV4R2
from tonutils.nft import CollectionEditableModified
from pytoniq_core import Address
from tonutils.nft import CollectionEditableModified, NFTEditableModified
from tonutils.nft.content import NFTModifiedOnchainContent
from tonutils.wallet import WalletV4R2

from dotenv import load_dotenv
import os

load_dotenv()  # подгружает переменные из .env

IS_TESTNET = os.getenv("IS_TESTNET") == "True"
MNEMONIC: list[str] = os.getenv('MNEMONIC').split()
COLLECTION_ADDRESS = os.getenv("COLLECTION_ADDRESS")



obj = {
    "characteristic": "Useful hateful",
    "type" : "carrot", #carrot/turnip/pig
    "img" : "https://raw.githubusercontent.com/MarchelloLemonchello/NFT-collection/refs/heads/main/output5.png" 

}

CURRENT_NFT_INDEX = -1
CURRENT_NFT_INDEX += 1

async def main() -> None:
    client = LiteserverClient(is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    nft = NFTEditableModified(
        index=CURRENT_NFT_INDEX,
        collection_address=Address(COLLECTION_ADDRESS),
    )
    body = CollectionEditableModified.build_mint_body(
        index=CURRENT_NFT_INDEX,
        owner_address=Address(wallet.address),
        content=NFTModifiedOnchainContent(
            name=obj["characteristic"] + " " + obj["type"],
            description=f"Non-Fungible Token confirming your rights to own a unique, unrepeatable virtual {obj['type']} from Network Farm Terminal. In short: NFT from NFT",
            image=obj["img"],
        ),
    )

    tx_hash = await wallet.transfer(
        destination=COLLECTION_ADDRESS,
        amount=0.02,
        body=body,
    )

    print(f"Successfully minted NFT with index {CURRENT_NFT_INDEX}: {nft.address.to_str()}")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())