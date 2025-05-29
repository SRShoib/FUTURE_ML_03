from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import pickle, re, nltk, tensorflow as tf, uvicorn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
import tensorflow as tf

# Paths
SRC_DIR    = Path(__file__).parent                   # .../Task 3/src
MODEL_DIR  = SRC_DIR.parent / 'saved_models'         # .../Task 3/saved_models
STATIC_DIR = SRC_DIR  / 'static'

MODEL_PATH = MODEL_DIR / 'intent_classifier.keras'
LABEL_PATH = MODEL_DIR / 'label_index.pkl'

# Load model & labels
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
with open(LABEL_PATH, 'rb') as f:
    label_index = pickle.load(f)

# NLP setup
nltk.download('stopwords')
nltk.download('wordnet')
STOPWORDS = set(stopwords.words('english'))
LEMMA     = WordNetLemmatizer()
TOKENIZER = TreebankWordTokenizer()

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = TOKENIZER.tokenize(text)
    cleaned = [
        LEMMA.lemmatize(tok)
        for tok in tokens
        if tok not in STOPWORDS and len(tok) > 2
    ]
    return " ".join(cleaned)

app = FastAPI()

# Serve static files at /static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve index.html at /
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")

# Prediction endpoint
@app.post("/predict_intent")
async def predict(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    proc = preprocess_text(msg)

    # wrap in a tf.Tensor of dtype string
    input_tensor = tf.constant([proc])            # shape (1,)

    # now Keras will recognize it as string input
    pred = model.predict(input_tensor)

    idx        = int(pred.argmax(axis=1)[0])
    intent     = label_index[idx]
    confidence = float(pred[0, idx])
    return {"intent": intent, "confidence": confidence}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
