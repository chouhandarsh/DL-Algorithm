from pathlib import Path
import json

import numpy as np
import tensorflow as tf

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(
    "/mnt/d/DL-Algorithm/projects/NextWordPredictor"
)

TOKEN_IDS_FILE = BASE_DIR / "data" / "token_ids.npy"
VOCAB_FILE = BASE_DIR / "data" / "vocab.json"

MODEL_FILE = BASE_DIR / "data" / "code_predictor.keras"


# --------------------------------------------------
# PARAMETERS
# --------------------------------------------------

SEQUENCE_LENGTH = 56
BATCH_SIZE = 64
EMBEDDING_DIM = 128
LSTM_UNITS = 256
EPOCHS = 10


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("Loading token IDs...")

token_ids = np.load(
    TOKEN_IDS_FILE,
    mmap_mode="r"
)

print("Total tokens:", len(token_ids))


# --------------------------------------------------
# LOAD VOCABULARY
# --------------------------------------------------

with open(VOCAB_FILE, "r", encoding="utf-8") as f:
    vocab_data = json.load(f)

vocab_size = len(vocab_data["token_to_id"])

print("Vocabulary size:", vocab_size)


# --------------------------------------------------
# CREATE TF DATASET
# --------------------------------------------------

dataset = tf.data.Dataset.from_tensor_slices(
    token_ids
)

dataset = dataset.window(
    SEQUENCE_LENGTH + 1,
    shift=1,
    drop_remainder=True
)

dataset = dataset.flat_map(
    lambda window:
        window.batch(SEQUENCE_LENGTH + 1)
)

dataset = dataset.map(
    lambda window: (
        window[:-1],
        window[-1]
    ),
    num_parallel_calls=tf.data.AUTOTUNE
)


# --------------------------------------------------
# BATCH
# --------------------------------------------------

dataset = dataset.batch(
    BATCH_SIZE
)

dataset = dataset.prefetch(
    tf.data.AUTOTUNE
)


# --------------------------------------------------
# CHECK DATA
# --------------------------------------------------

for X, y in dataset.take(1):

    print()
    print("X shape:", X.shape)
    print("y shape:", y.shape)

    print()
    print("First input:")
    print(X[0].numpy())

    print()
    print("Target:")
    print(y[0].numpy())


# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = Sequential([

    Input(
        shape=(SEQUENCE_LENGTH,)
    ),

    Embedding(
        input_dim=vocab_size,
        output_dim=EMBEDDING_DIM
    ),

    LSTM(
        LSTM_UNITS
    ),

    Dense(
        vocab_size,
        activation="softmax"
    )
])


# --------------------------------------------------
# COMPILE
# --------------------------------------------------

model.compile(
    optimizer="adam",

    loss="sparse_categorical_crossentropy",

    metrics=["accuracy"]
)


model.summary()


# --------------------------------------------------
# TRAIN
# --------------------------------------------------

history = model.fit(
    dataset,
    epochs=EPOCHS
)


# --------------------------------------------------
# SAVE
# --------------------------------------------------

model.save(MODEL_FILE)

print()
print("Model saved to:")
print(MODEL_FILE)