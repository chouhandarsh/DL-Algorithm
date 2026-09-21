from pathlib import Path
import json
import numpy as np


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(
    "/mnt/d/DL-Algorithm/projects/NextWordPredictor"
)

TOKENS_FILE = BASE_DIR / "tokens.txt"
VOCAB_FILE = BASE_DIR / "data" / "vocab.json"
TOKEN_IDS_FILE = BASE_DIR / "data" / "token_ids.npy"


# --------------------------------------------------
# LOAD VOCABULARY
# --------------------------------------------------

print("Loading vocabulary...")

with open(VOCAB_FILE, "r", encoding="utf-8") as f:
    vocab_data = json.load(f)

token_to_id = vocab_data["token_to_id"]

print("Vocabulary size:", len(token_to_id))


# --------------------------------------------------
# READ TOKENS
# --------------------------------------------------

print("Reading tokens...")

with open(TOKENS_FILE, "r", encoding="utf-8") as f:
    tokens = f.read().split()

print("Total tokens:", len(tokens))


# --------------------------------------------------
# TOKEN → ID
# --------------------------------------------------

print("Converting tokens to IDs...")
unk_id = token_to_id["<UNK>"]
token_ids = np.array(
    [
        token_to_id.get(token, unk_id)
        for token in tokens
    ],
    dtype=np.int32
)


# --------------------------------------------------
# SAVE
# --------------------------------------------------

np.save(
    TOKEN_IDS_FILE,
    token_ids
)


print()
print("Conversion completed.")
print("Shape:", token_ids.shape)
print("Saved to:", TOKEN_IDS_FILE)