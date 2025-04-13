import pyvista as pv
import numpy as np
import cv2
from rembg import remove
from PIL import Image
from io import BytesIO

def remove_background(image_path):
    try:
        with open(image_path, "rb") as input_file:
            input_image = input_file.read()
        output_image = remove(input_image)
        output_image_pil = Image.open(BytesIO(output_image))
        return np.array(output_image_pil)
    except Exception as e:
        print(f"Error during background removal: {e}")
        return None

def depth_map_to_3d_with_texture(image_array, depth_scale=0.00):
    depth_map = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    depth_map = depth_map.astype(np.float32) / 255.0
    h, w = depth_map.shape
    x, y = np.linspace(0, 1, w), np.linspace(0, 1, h)
    xv, yv = np.meshgrid(x, y)
    z = depth_map * depth_scale
    points = np.c_[xv.ravel(), yv.ravel(), z.ravel()]
    grid = pv.PolyData(points).delaunay_2d()
    if not grid.faces.size:
        raise ValueError("Mesh generation failed. No faces created.")
    uv_coords = np.c_[xv.ravel(), yv.ravel()].astype(np.float32)
    grid.point_data["Texture Coordinates"] = uv_coords
    grid.active_texture_coordinates = uv_coords
    return grid

def visualize_3d_model_with_texture(grid, texture_image):
    texture = pv.Texture(texture_image)
    plotter = pv.Plotter()
    plotter.add_mesh(grid, texture=texture, show_edges=False)
    plotter.show()
