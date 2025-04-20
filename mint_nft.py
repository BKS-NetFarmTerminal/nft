from tonutils.client import LiteserverClient
from tonutils.wallet import WalletV4R2
from tonutils.nft import CollectionEditableModified
from pytoniq_core import Address
from tonutils.nft import CollectionEditableModified, NFTEditableModified
from tonutils.nft.content import NFTModifiedOnchainContent
from tonutils.wallet import WalletV4R2


from dotenv import load_dotenv
import os

load_dotenv()


async def mint_nft(characteristic, nft_type, img, is_testnet, new_owner_address):

    client = LiteserverClient(is_testnet=is_testnet)

    collection_info = await client.run_get_method(os.getenv("COLLECTION_ADDRESS"), "get_collection_data")
    index = collection_info[0]

    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, os.getenv('MNEMONIC_MINTER').split())

    nft = NFTEditableModified(
        index=index,
        collection_address=Address(os.getenv("COLLECTION_ADDRESS")),
    )
    body = CollectionEditableModified.build_mint_body(
        index=index,
        owner_address=new_owner_address,
        content=NFTModifiedOnchainContent(
            name=characteristic + " " + nft_type,
            description=f"Non-Fungible Token confirming your rights to own a unique, unrepeatable virtual {nft_type} from Network Farm Terminal. In short: NFT from NFT",
            image=img,
        ),
        # forward_payload=(
        #     begin_cell()
        #     .store_uint(0, 32)
        #     .store_snake_string(comment)
        #     .end_cell()
        # ),
    )

    tx_hash = await wallet.transfer(
        destination=os.getenv("COLLECTION_ADDRESS"),
        amount=0.1,
        body=body,
    )
    nft_addr = await client.run_get_method(os.getenv("COLLECTION_ADDRESS"), "get_nft_address_by_index", stack=[index])
    nft_addr = f"{nft_addr[0]}"[8:-1]
    print(f"Successfully minted NFT with index {index}: {nft_addr}")
    print(f"Transaction hash: {tx_hash}")
    return nft_addr