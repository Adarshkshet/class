import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyvista as pv

# Load the model from MiDaS
model_type = "DPT_Large"  # or "DPT_Hybrid" based on your preference
midas = torch.hub.load("intel-isl/MiDaS", model_type)
midas.eval()

# Load transforms for the model
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.dpt_transform if model_type in ["DPT_Large", "DPT_Hybrid"] else midas_transforms.small_transform

# Load and transform input image
image_path = 'Back.png'  # Replace with your image path
input_image = Image.open(image_path)
input_batch = transform(input_image).to('cpu')  # or 'cuda' if GPU is available

# Run the model to get the depth map
with torch.no_grad():
    prediction = midas(input_batch)
    depth_map = prediction.squeeze().cpu().numpy()

# Visualize the depth map
plt.imshow(depth_map, cmap='gray')
plt.title("Depth Map")
plt.colorbar()
plt.show()

# ----- Code to Add 3D Visualization -----

# Convert depth map to a 3D mesh
height, width = depth_map.shape
x = np.linspace(0, 1, width)
y = np.linspace(0, 1, height)
X, Y = np.meshgrid(x, y)
Z = depth_map  # Use the depth map values as the Z-axis

# Create structured grid
grid = pv.StructuredGrid(X, Y, Z)

# Optional: Apply texture if you have an image
texture_image = Image.open(image_path)
texture = pv.numpy_to_texture(np.array(texture_image))

# Create a PyVista plotter for 3D visualization
plotter = pv.Plotter()
plotter.add_mesh(grid, texture=texture, cmap='viridis')
plotter.add_scalar_bar(title="Depth")

# Show the 3D visualization
plotter.show()
