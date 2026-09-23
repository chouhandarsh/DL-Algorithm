from pathlib import Path
from collections import Counter
import json

BASE_DIR = Path(
    "/mnt/d/DL-Algorithm/projects/NextWordPredictor"
)

TOKENS_FILE = BASE_DIR / "tokens.txt"
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

VOCAB_FILE = DATA_DIR / "vocab.json"


# Read the complete token stream
with open(TOKENS_FILE, "r", encoding="utf-8") as f:
    tokens = f.read().split()

print("Total token occurrences:", len(tokens))


# Count how frequently every token occurs
counter = Counter(tokens)

print("Unique tokens:", len(counter))


# Keep only the most frequent tokens
MAX_VOCAB_SIZE = 50000

most_common = counter.most_common(MAX_VOCAB_SIZE)

vocab = [token for token, count in most_common]

print("Final vocabulary size:", len(vocab))


# Add an unknown token
if "<UNK>" not in vocab:
    vocab.append("<UNK>")


# Create mappings
token_to_id = {
    token: i
    for i, token in enumerate(vocab)
}

id_to_token = {
    i: token
    for token, i in token_to_id.items()
}


# Save
with open(VOCAB_FILE, "w", encoding="utf-8") as f:
    json.dump(
        {
            "token_to_id": token_to_id,
            "id_to_token": {
                str(k): v
                for k, v in id_to_token.items()
            }
        },
        f,
        ensure_ascii=False
    )


print("Vocabulary saved to:", VOCAB_FILE)