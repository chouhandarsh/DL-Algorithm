from fastapi import FastAPI
import pickle
from fastapi.responses import FileResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from fastapi.staticfiles import StaticFiles
app = FastAPI()
model = load_model("siamese_model.keras")
with open("tokenizer.pkl",'rb') as f:
    tokenizer = pickle.load(f)
MAX_LEN= 50
def preprocess(text):

    sequence = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post",
        truncating="post"
    )

    return padded
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def home():
    return FileResponse("static/index.html")
@app.post("/predict")
def predict(
    text_a: str,
    text_b = str
):
    input_a = preprocess(text_a)
    input_b = preprocess(text_b)
    prediction  = model.predict(
        [input_a,input_b],
        verbose =0
    )
    score = float(prediction[0][0])
    return {
        "score":score
    }
