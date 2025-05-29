import os
import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import pickle

# Load preprocessed data
df = pd.read_pickle(r'D:\Research\Topics\Future Interns\FUTURE_ML_03\data\processed\customer_support_tickets_preprocessed.pkl')
texts = df['tokens'].map(" ".join).tolist()   # list[str]
labels = df['intent'].astype('category')
label_index = dict(enumerate(labels.cat.categories))
y = tf.keras.utils.to_categorical(labels.cat.codes)  # np.ndarray, shape (N, num_intents)

# TextVectorization
vectorizer = layers.TextVectorization(
    max_tokens=10000,
    output_sequence_length=50
)
vectorizer.adapt(texts)

# Build model
model = tf.keras.Sequential([
    vectorizer,
    layers.Embedding(input_dim=10000, output_dim=64),
    layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
    layers.Bidirectional(layers.LSTM(32)),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(y.shape[1], activation='softmax'),
])
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Create a tf.data.Dataset and split into train/val
dataset = tf.data.Dataset.from_tensor_slices((texts, y))
dataset = dataset.shuffle(buffer_size=len(texts), seed=42)  # shuffle all

train_size = int(0.8 * len(texts))
train_ds = (
    dataset
    .take(train_size)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)
val_ds = (
    dataset
    .skip(train_size)
    .batch(32)
    .prefetch(tf.data.AUTOTUNE)
)

# Train
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=30
)

# Save
save_dir = r'D:\Research\Topics\Future Interns\FUTURE_ML_03\saved_models'
os.makedirs(save_dir, exist_ok=True)

# Save in native Keras format (recommended)
model.save(os.path.join(save_dir, 'intent_classifier.keras'))

# Save your label map
with open(os.path.join(save_dir, 'label_index.pkl'), 'wb') as f:
    pickle.dump(label_index, f)

print("✔ Training complete — model saved to:")
print("   •", os.path.join(save_dir, 'intent_classifier.keras'))
print("   •", os.path.join(save_dir, 'label_index.pkl'))
