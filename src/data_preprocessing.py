import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
import pandas as pd

nltk.download('stopwords')
nltk.download('wordnet')

STOPWORDS = set(stopwords.words('english'))
LEMMA = WordNetLemmatizer()
TOKENIZER = TreebankWordTokenizer()

def preprocess_text(text: str) -> list[str]:
    """
    1. Lowercase
    2. Remove non-alphanumeric
    3. Simple Treebank tokenization
    4. Remove stopwords & short tokens
    5. Lemmatize
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = TOKENIZER.tokenize(text)
    return [
        LEMMA.lemmatize(tok)
        for tok in tokens
        if tok not in STOPWORDS and len(tok) > 2
    ]

if __name__ == "__main__":
    # Load your support tickets CSV
    df = pd.read_csv(r"D:\Research\Topics\Future Interns\FUTURE_ML_03\data\raw\customer_support_tickets.csv")

    # Select & rename columns
    df = df[['Ticket Description', 'Ticket Type']].dropna()
    df.columns = ['utterance', 'intent']

    # Preprocess and save tokens
    df['tokens'] = df['utterance'].map(preprocess_text)
    df.to_pickle(r'D:\Research\Topics\Future Interns\FUTURE_ML_03\data\processed\customer_support_tickets_preprocessed.pkl')
    print("✔ Preprocessed data saved to \FUTURE_ML_03\data\processed\customer_support_tickets_preprocessed.pkl")
