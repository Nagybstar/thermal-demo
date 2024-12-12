from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a simple HTML template with two buttons
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Image Upload and List App</title>
</head>
<body>
    <h1>Image Actions</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="file">Upload an image:</label>
        <input type="file" name="file" id="file" accept="image/*" required>
        <button type="submit">Upload Image</button>
    </form>
    <form action="/list" method="get">
        <button type="submit">List Uploaded Images</button>
    </form>
    <p>{{ message }}</p>
    {% if images %}
    <h2>Uploaded Images:</h2>
    <ul>
        {% for image in images %}
        <li>{{ image }}</li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(template, message="", images=None)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        message = "No file part"
        return render_template_string(template, message=message, images=None)

    file = request.files['file']
    if file.filename == '':
        message = "No selected file"
        return render_template_string(template, message=message, images=None)

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        message = f"Image '{filename}' uploaded successfully!"
        return render_template_string(template, message=message, images=None)

@app.route('/list', methods=['GET'])
def list_images():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(template, message="Uploaded images listed below:", images=images)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
