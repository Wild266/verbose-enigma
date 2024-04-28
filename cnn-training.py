from sklearn.metrics import accuracy_score, log_loss, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from keras import layers, models
import pandas as pd
import numpy as np

def create_othello_cnn():
    model = models.Sequential([
      layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(8, 8, 2)),
      layers.BatchNormalization(),
      layers.MaxPooling2D((2, 2)),
      layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
      layers.BatchNormalization(),
      layers.MaxPooling2D((2, 2)),
      layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
      layers.BatchNormalization(),
      layers.GlobalAveragePooling2D(),
      layers.Dense(128, activation='relu'),
      layers.Dropout(0.5),
      layers.Dense(64, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def preprocess_data(df):
  # Assuming 'X' needs to be evaluated from a string if stored as such
  if isinstance(df['X'].iloc[0], str):
    df['X'] = df['X'].apply(eval)  # Convert from string to actual list
  
  # Ensure 'y' is also correctly formatted, handling NaN values properly
  if isinstance(df['y'].iloc[0], str):
    df['y'] = df['y'].apply(eval)  # Convert from string to actual list

  # Convert list of lists to a numpy array and reshape
  try:
    X = np.array(df['X'].tolist()).reshape(-1, 8, 8, 1)
  except ValueError as e:
    print("Error reshaping X:", e)
    print("Shape of array attempted to reshape:", np.array(df['X'].tolist()).shape)
    raise

  # Handling 'player'
  player = np.array(df['player']).reshape(-1, 1, 1, 1)
  player = np.tile(player, (1, 8, 8, 1))
  inputs = np.concatenate([X, player], axis=-1)

  # Flatten 'y' and prepare it for model output
  try:
    y = np.array(df['y'].tolist()).reshape(-1, 64)
  except ValueError as e:
    print("Error reshaping y:", e)
    print("Shape of array attempted to reshape:", np.array(df['y'].tolist()).shape)
    raise

  return inputs, y

# Load data
data = pd.read_csv('preprocessed_dataset.csv')

train_df, test_df = train_test_split(data, test_size=0.2, random_state=42)
X_train, y_train = preprocess_data(train_df)
X_test, y_test = preprocess_data(test_df)

# Create and train the model
model = create_othello_cnn()
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
model.save_weights('/work/users/j/a/jackg/othello_model.weights.h5')

# Predict on the test set
predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)
true_classes = np.argmax(y_test, axis=1)

# Calculate metrics
accuracy = accuracy_score(true_classes, predicted_classes)
cross_entropy_loss = log_loss(true_classes, predicted_classes)
report = classification_report(true_classes, predicted_classes, target_names=[f"Move {i+1}" for i in range(64)])

# Open a file to save the outputs
with open('/work/users/j/a/jackg/othello_model_evaluation_report.txt', 'w') as f:
  f.write(f"Accuracy: {accuracy}\n")
  f.write(f"Cross-Entropy Loss: {cross_entropy_loss}\n")
  f.write("Classification Report:\n")
  f.write(report + "\n")

  cm = confusion_matrix(true_classes, predicted_classes)
  np.savetxt(f, cm, fmt='%d', header='Confusion Matrix:')
