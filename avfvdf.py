from PIL import Image
import matplotlib.pyplot as plt

# Load the image
img_path = 'Jet.png'  # Replace with your image path
try:
    img = Image.open(img_path)
    img.show()  # Display the image using PIL's built-in viewer
except Exception as e:
    print(f"Error loading image: {e}")

# Optionally, display it using matplotlib to verify it's loaded
plt.imshow(img)
plt.title("Loaded Image")
plt.axis('off')  # Hide axes
plt.show()
