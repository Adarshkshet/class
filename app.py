from flask import Flask, render_template, request, redirect, url_for
import os
from DynamicRotation import remove_background, depth_map_to_3d_with_texture, visualize_3d_model_with_texture
import pyvista as pv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part in the request"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process the uploaded file
            background_removed = remove_background(file_path)
            if background_removed is None:
                return "Background removal failed"

            try:
                grid = depth_map_to_3d_with_texture(background_removed, depth_scale=0.00)
                visualize_3d_model_with_texture(grid, background_removed)
                return "3D visualization displayed"
            except Exception as e:
                return f"Error: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
