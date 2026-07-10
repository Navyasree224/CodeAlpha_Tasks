from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

# Load dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Print original shapes
print("Original Training Shape:", X_train.shape)
print("Original Testing Shape :", X_test.shape)

# Normalize images
X_train = X_train / 255.0
X_test = X_test / 255.0

# Reshape images for CNN
X_train = X_train.reshape(60000, 28, 28, 1)
X_test = X_test.reshape(10000, 28, 28, 1)

# Print new shapes
print("\nAfter Preprocessing")
print("Training Shape:", X_train.shape)
print("Testing Shape :", X_test.shape)

# Display first image
plt.imshow(X_train[0].reshape(28,28), cmap="gray")
plt.title(f"Label: {y_train[0]}")
plt.axis("off")
plt.show()