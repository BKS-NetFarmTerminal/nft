from tonutils.client import LiteserverClient
from tonutils.utils import to_nano
from tonutils.wallet import WalletV4R2
from tonutils.nft import CollectionEditableModified
from tonutils.nft.content import CollectionModifiedOnchainContent
from tonutils.nft.royalty_params import RoyaltyParams

from dotenv import load_dotenv
import os

load_dotenv()  # подгружает переменные из .env

IS_TESTNET = os.getenv("IS_TESTNET") == "True"
MNEMONIC: list[str] = os.getenv('MNEMONIC').split()

async def main() -> None:
    client = LiteserverClient(is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)
    print(wallet.address)

    collection = CollectionEditableModified(
        owner_address=wallet.address,
        next_item_index=0,
        content=CollectionModifiedOnchainContent(
            name="Network Farm Terminal ledger test1",
            description="Non-Fungible Tokens that confirm the property of Network Farm Terminal farmers, such as unique, unrepeatable, animals and plants grown by their hands, namely, fingers typing code on a keyboard in a terminal",
            image="https://ibb.co/wNSDyqWs",
        ),
        royalty_params=RoyaltyParams(
            base=1000,
            factor=50,
            address=wallet.address,
        ),
    )

    tx_hash = await wallet.transfer(
        destination=collection.address,
        amount=0.05,
        state_init=collection.state_init,
    )

    print(f"Successfully deployed NFT Collection at address: {collection.address.to_str()}")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
