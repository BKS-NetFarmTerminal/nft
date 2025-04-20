from flask import Flask, jsonify, request
import asyncio
from make_nft import make_nft_please


app = Flask(__name__)

@app.route('/mint_nft', methods=['POST'])
async def post_example():
    """
    {
        "nft_type": "",
        "user_address": ""
    }
    """
    content = request.get_json()
    nft_type = content["nft_type"] 
    user_address = content["user_address"]

    [nft_url, img_url, nft_name, ] = await make_nft_please(nft_type, user_address)
    body = {
        "nft_url" : nft_url,
        "img_url" : img_url,
        "nft_name" : nft_name
    }
    return jsonify(body), 201


if __name__ == '__main__':
    app.run(debug=True)
