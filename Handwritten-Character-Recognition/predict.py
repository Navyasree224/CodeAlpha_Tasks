import numpy as np
from tensorflow.keras.models import load_model

# Load the trained model only once
model = load_model("handwritten_model.keras")

def predict_digit(image):
    """
    Predicts a handwritten digit.

    Parameters:
        image (numpy array): Shape (28,28)

    Returns:
        predicted_digit (int)
        confidence (float)
        probabilities (numpy array)
    """

    # Normalize
    image = image.astype("float32") / 255.0

    # Reshape
    image = image.reshape(1, 28, 28, 1)

    # Predict
    prediction = model.predict(image, verbose=0)

    digit = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return digit, confidence, prediction[0]