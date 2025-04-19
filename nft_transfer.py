from pytoniq_core import Address, begin_cell
from tonutils.client import LiteserverClient
from tonutils.nft import NFTStandard
from tonutils.wallet import WalletV4R2

from dotenv import load_dotenv
import os

load_dotenv()  # подгружает переменные из .env


# Set to True for test network, False for main network
IS_TESTNET = os.getenv("IS_TESTNET") == "True"
MNEMONIC: list[str] = os.getenv('MNEMONIC').split()

# Address of the NFT to be transferred and the new owner address

obj = {
    "user_address": "0QCHMichcLkuC5OHon0YTBDGMaNdTNbBB2kS2LnZ9a8lExBa",
    "NFT_address": "kQA6XjzFS9xLFNL0Ph2OwV5rcbczYAwBTP7OPNTD7XcvuV3v"
}


NFT_ADDRESS = obj["NFT_address"]
NEW_OWNER_ADDRESS = obj["user_address"]

# Optional comment to include in the forward payload
COMMENT = "Hello from tonutils!"


async def main() -> None:
    client = LiteserverClient(is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    body = NFTStandard.build_transfer_body(
        new_owner_address=Address(NEW_OWNER_ADDRESS),
        forward_payload=(
            begin_cell()
            .store_uint(0, 32)
            .store_snake_string(COMMENT)
            .end_cell()
        ),
        forward_amount=1,
    )

    tx_hash = await wallet.transfer(
        destination=NFT_ADDRESS,
        amount=0.05,
        body=body,
    )

    print(f"Successfully transferred NFT from address {NFT_ADDRESS} to new owner {NEW_OWNER_ADDRESS}.")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())