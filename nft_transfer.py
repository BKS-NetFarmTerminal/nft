from pytoniq_core import Address, begin_cell
from tonutils.client import LiteserverClient
from tonutils.nft import NFTStandard
from tonutils.wallet import WalletV4R2

from dotenv import load_dotenv
import os

load_dotenv()  # подгружает переменные из .env


# Set to True for test network, False for main network
IS_TESTNETc = os.getenv("IS_TESTNET") == "True"
MNEMONICc: list[str] = os.getenv('MNEMONIC').split()

# Address of the NFT to be transferred and the new owner address

objj = {
    "user_address": "0QCHMichcLkuC5OHon0YTBDGMaNdTNbBB2kS2LnZ9a8lExBa",
    "NFT_address": "kQA6XjzFS9xLFNL0Ph2OwV5rcbczYAwBTP7OPNTD7XcvuV3v"
}




# Optional comment to include in the forward payload



async def nft_transfer(new_owner_address, nft_address, is_testnet,):
    comment = "hi!"
    client = LiteserverClient(is_testnet=is_testnet)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, os.getenv('MNEMONIC').split())

    body = NFTStandard.build_transfer_body(
        new_owner_address=Address(new_owner_address),
        forward_payload=(
            begin_cell()
            .store_uint(0, 32)
            .store_snake_string(comment)
            .end_cell()
        ),
        forward_amount=1,
    )

    tx_hash = await wallet.transfer(
        destination=nft_address,
        amount=0.05,
        body=body,
    )

    print(f"Successfully transferred NFT from address {nft_address} to new owner {new_owner_address}.")
    print(f"Transaction hash: {tx_hash}")
    return "success"


if __name__ == "__main__":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())