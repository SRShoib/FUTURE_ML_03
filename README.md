# Customer Support Chatbot

A simple NLP-powered chatbot that can answer basic customer support queries.  
Built with TensorFlow/Keras for intent classification, FastAPI for the backend API, and a modern HTML/CSS/JavaScript frontend.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Directory Structure](#directory-structure)  
5. [Dataset](#dataset)  
6. [Model Training](#model-training)  
7. [Running the API & Web UI](#running-the-api--web-ui)  
8. [Usage](#usage)  
9. [Future Improvements](#future-improvements)  
10. [License](#license)  

---

## 📝 Project Overview

Customer support teams often get inundated with repetitive questions—order status, returns, refunds, technical issues, and more. This project demonstrates:

- **Natural Language Processing (NLP)** to classify user intent.  
- **Chatbot development** to automatically respond to common queries.  
- **User interaction design** via a clean, responsive web interface.

---

## ✨ Features

- **Intent Classification** using a TensorFlow/Keras model.  
- **FastAPI** backend with a `/predict_intent` endpoint.  
- **Interactive Web UI** built with HTML/CSS/JavaScript (no frameworks).  
- **Quick-Reply Buttons** for common questions.  
- **Fallback & Confidence Display** for unrecognized intents.  
- **Easy-to-Extend** mapping of intents to human-friendly responses.

---

## 🛠️ Tech Stack

| Layer          | Technology                                           |
| -------------- | ---------------------------------------------------- |
| Model Training | Python, TensorFlow/Keras, NLTK                       |
| Backend/API    | Python, FastAPI, Uvicorn                             |
| Frontend       | HTML5, CSS3, Vanilla JavaScript                      |
| Versioning     | Git, GitHub                                          |

---

## 📂 Directory Structure

FUTURE_ML_03/
├── data/
│   ├── raw/  
│   │   └── customer_support_tickets.csv           # Original export of chat/FAQ logs
│   ├── processed/  
│   │   └── customer_support_tickets_preprocessed.pkl
│
├── saved_models/
│   ├── intent_classifier/          # Saved TensorFlow model directory
│   └── label_index.pkl             # Pickled mapping from class indices to intent names
│
├── src/                            # Application code
│   ├── data_preprocessing.py       # Text cleaning & tokenization
│   ├── intent_model.py             # Model definition & training script
│   ├── app.py                      # FastAPI webhook server
│   ├── analytics.py                # Pandas + Matplotlib analysis scripts
│   └── static/                     # Web UI assets
│       ├─ index.html
│       ├─ styles.css
│       └─ script.js
│

customer-support-chatbot/
├── app.py                        # Flask backend application
├── static/
│   ├── styles.css                # CSS styling for the web interface
│   └── script.js                 # JavaScript for frontend interactivity
├── templates/
│   └── index.html                # HTML template for the web interface
├── model.pkl                     # Saved model (generated after training)
├── customer_support_tickets.csv  # Dataset (already included)
└── requirements.txt              # Python dependencies

---

## 📖 Dataset

- Download the Customer Support Ticket Dataset from [Kaggle](https://www.kaggle.com/datasets/waseemalastal/customer-support-ticket-dataset)
   - Place the CSV file in the project root directory as `customer_support_tickets.csv`

This CSV of historical customer support tickets (`customer_support_tickets.csv`), containing columns such as:

- **`utterance`**: the raw customer message  
- **`intent`**: the labeled intent category

Data was preprocessed (tokenized, stopwords removed, lemmatized) before training a simple feed-forward or LSTM model in Keras.

---

## 🏋️ Model Training

1. **Preprocess text** (in `data_preprocessing.py`):
   ```bash
   python data_preprocessing.py
   ```
2. **Train intent classifier** (in `intent_model.py`):
   ```bash
   python intent_model.py
   ```
   - The model is saved in **Keras** format to `saved_models/intent_classifier.keras`.  
   - Label mapping (intent → index) saved as `label_index.pkl`.

---

## 🚀 Running the API & Web UI

   ```
1. **Start the server**:
   ```bash
   uvicorn app:app --reload
   ```
2. **Open** your browser at [http://localhost:8000/](http://localhost:8000/) to view the chat UI.

---

## 🔧 Usage

- **Free-text**: Type any question (e.g. “Where’s my order?”, “I need a refund.”) and hit Enter or click the ➤ button.  
- **Quick Replies**: Click one of the suggested buttons (Order Status, Return Policy, Technical Issue, Refund request).  
- **Response**: The bot displays a pre-configured answer with a confidence score.

---

## 🚧 Future Improvements

- **Add more intents** (e.g. shipping times, account management).  
- **Dynamic response generation** using slot-filling or a retrieval-based approach.  
- **Database integration** for real-time order lookups.  
- **Authentication** and user context (session tracking).  
- **Dockerize** the entire app for easy deployment.

---


*Happy coding!*
