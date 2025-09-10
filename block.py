import os
import json
import hashlib
import time
import shutil

#defining folder locations
#where transactions are waiting
#where they go after being included in a block
#where the block files are saved
PENDING_DIR = "pending_transactions"
PROCESSED_DIR = "processed_transactions"
BLOCKS_DIR = "blocks"

#taking a string, encoding it and returning its SHA256 hash
def sha256(content: str) -> str:
    """Return SHA-256 hash of given string."""
    return haslib.sha256(content.encode("utf-8")).hexdigest()

#finding where the blockchain is and returning highest height
def get_latest_block():
    """Find the latest block file and return its data and height."""
    if not os.path.exists(BLOCKS_DIR):
        return None, -1, "N/A"

    block_files = [f for f in os.listdir(BLOCKS_DIR) if f.endswith(".json")]
    if not block_files:
        return None, -1, "N/A"

    lastest_block = None
    latest_hieght = -1
    lastest_hash = "N/A"

#reading each block file and checking its height
    for filename in block_files:
        with open(os.path.join.(BLOCKS_DIR, filename), "r") as f:
            data = json.load(f)
            height = data["header"]["height"]
            if height > latest_height:
                latest_height = height
                latest_block = data
                latest_hash = filename.replace(".jason", "")

    return latest_block, lastest_height, latest_hash
    