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
def sha256_hash(content: str) -> str:
    """Return SHA-256 hash of given string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

#finding where the blockchain is and returning highest height
def get_latest_block():
    """Find the latest block file and return its data and height."""
    if not os.path.exists(BLOCKS_DIR):
        return None, -1, "N/A"

    block_files = [f for f in os.listdir(BLOCKS_DIR) if f.endswith(".json")]
    if not block_files:
        return None, -1, "N/A"

    latest_block = None
    latest_height = -1
    latest_hash = "N/A"

#reading each block file and checking its height
    for filename in block_files:
        with open(os.path.join(BLOCKS_DIR, filename), "r") as f:
            data = json.load(f)
            height = data["header"]["height"]
            if height > latest_height:
                latest_height = height
                latest_block = data
                latest_hash = filename.replace(".json", "")

    return latest_block, latest_height, latest_hash
    

def load_pending_transactions():
    """Load pending transactions from folder."""
    if not os.path.exists(PENDING_DIR):
        os.makedirs(PENDING_DIR)

    tx_files = [f for f in os.listdir(PENDING_DIR) if f.endswith(".json")]
    transactions = []

    for filename in tx_files:
        filepath = os.path.join(PENDING_DIR, filename)
        with open(filepath, "r") as f:
            content = json.load(f)

        transactions.append({
            "hash": filename.replace(".json", ""),
            "content": content
        })

    return transactions, tx_files

def create_block(transactions, prev_hash, height):
    """Create a block object with header and body."""
    body = transactions
    body_str = json.dumps(body, separators = (",", ":"))
    body_hash = sha256_hash(body_str)

    header = {
        "height": height, 
        "timestamp": int(time.time()), 
        "previousblock": prev_hash,
        "hash": body_hash
    }

    block = {
        "header": header, 
        "body": body
    }

    #for filename baed on the header
    header_str = json.dumps(header, separators=(",", ":"))
    block_hash = sha256_hash(header_str)

    return block, block_hash

def save_block(block, block_hash):
    """Save block to file."""

    if not os.path.exists(BLOCKS_DIR):
        os.makedirs(BLOCKS_DIR)

    filepath = os.path.join(BLOCKS_DIR, f"{block_hash}.json")
    with open(filepath, "w") as f:
        json.dump(block, f, separators = (",", ":"))

    print(f"Completed, Block save as {filepath}")

def move_transactions(tx_files):
    """Move processed transactions to processed folder."""
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    for filename in tx_files:
        src = os.path.join(PENDING_DIR, filename)
        dst = os.path.join(PROCESSED_DIR, filename)
        shutil.move(src, dst)

def main():
    transactions, tx_files = load_pending_transactions()

    if not transactions:
        print("Error, no pending transactions to process.")
        return

    _, last_height, last_hash = get_latest_block()
    new_height = last_height + 1

    block, block_hash = create_block(transactions, last_hash, new_height)
    save_block(block, block_hash)
    move_transactions(tx_files)

if __name__ == "__main__":
    while True:
        cmd = input("\nPress ENTER to create a new block from pending transaction (or type 'exit' to quit): ")
        if cmd.lower() == "exit":
            break
        main()