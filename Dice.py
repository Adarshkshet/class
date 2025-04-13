import pyvista as pv
import numpy as np
from PIL import Image

# Function to resize images to a square, fitting each face of the cube
def load_and_resize_image(image_path, size=(512, 512)):
    img = Image.open(image_path)
    img = img.resize(size)  # Resize the image to fit the cube face
    return np.array(img)

# Load and resize images for each face
front_img = load_and_resize_image('Front.png')
back_img = load_and_resize_image('Back.png')
left_img = load_and_resize_image('Left.png')
right_img = load_and_resize_image('Right.png')
top_img = load_and_resize_image('Top.png')
bottom_img = load_and_resize_image('Bottom.png')

# Create PyVista textures from the resized images
textures = {
    "front": pv.Texture(front_img),
    "back": pv.Texture(back_img),
    "left": pv.Texture(left_img),
    "right": pv.Texture(right_img),
    "top": pv.Texture(top_img),
    "bottom": pv.Texture(bottom_img)
}

# Initialize the plotter
plotter = pv.Plotter()

# Helper function to create a face with texture coordinates
def create_textured_face(points):
    face = pv.PolyData(points, [[4, 0, 1, 2, 3]])
    # Define texture coordinates for each corner
    face.active_t_coords = np.array([
        [1, 0],  # Top-right
        [0, 0],  # Top-left
        [0, 1],  # Bottom-left
        [1, 1]   # Bottom-right
    ])
    return face

# Define cube faces with specific textures

# Front face
front_points = np.array([[0.5, -0.5, 0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5]])
front = create_textured_face(front_points)
plotter.add_mesh(front, texture=textures["front"])

# Back face
back_points = np.array([[0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5]])
back = create_textured_face(back_points)
plotter.add_mesh(back, texture=textures["back"])

# Left face
left_points = np.array([[-0.5, -0.5, 0.5], [-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5]])
left = create_textured_face(left_points)
plotter.add_mesh(left, texture=textures["left"])

# Right face
right_points = np.array([[0.5, -0.5, -0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5]])
right = create_textured_face(right_points)
plotter.add_mesh(right, texture=textures["right"])

# Top face
top_points = np.array([[-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5]])
top = create_textured_face(top_points)
plotter.add_mesh(top, texture=textures["top"])

# Bottom face
bottom_points = np.array([[0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5]])
bottom = create_textured_face(bottom_points)
plotter.add_mesh(bottom, texture=textures["bottom"])

# Show the plot with textured cube
plotter.show()
