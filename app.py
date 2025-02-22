import os
import cv2
import numpy as np
from sklearn.cluster import KMeans
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload folder setup
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to process image
def process_image(filepath, k=5, max_size=300, sample_size=5000):
    # Image load aur preprocess
    photo = cv2.imread(filepath)
    photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)

    # Resize image for speed
    height, width = photo.shape[:2]
    if max(height, width) > max_size:
        scale = max_size / max(height, width)
        photo = cv2.resize(photo, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    pixels = photo.reshape(-1, 3)

    # Sampling for speed
    if len(pixels) > sample_size:
        indices = np.random.choice(len(pixels), sample_size, replace=False)
        sampled_pixels = pixels[indices]
    else:
        sampled_pixels = pixels

    # Train K-means
    kmeans = KMeans(n_clusters=k, random_state=0, max_iter=5, n_init=1)
    kmeans.fit(sampled_pixels)
    labels = kmeans.predict(pixels)
    main_colors = kmeans.cluster_centers_.astype(int)

    # Clustered image
    clustered_image = main_colors[labels].reshape(photo.shape).astype(np.uint8)

    # Save images
    os.makedirs(RESULT_FOLDER, exist_ok=True)
    original_path = os.path.join(RESULT_FOLDER, 'original.png')
    clustered_path = os.path.join(RESULT_FOLDER, 'clustered.png')
    cv2.imwrite(original_path, cv2.cvtColor(photo, cv2.COLOR_RGB2BGR))
    cv2.imwrite(clustered_path, cv2.cvtColor(clustered_image, cv2.COLOR_RGB2BGR))

    return original_path, clustered_path, main_colors

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file uploaded")
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No file selected")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            k = int(request.form.get('k', 5))
            original_path, clustered_path, main_colors = process_image(filepath, k)

            return render_template('index.html', 
                                  original_path=original_path.split('static/')[1],
                                  clustered_path=clustered_path.split('static/')[1],
                                  colors=main_colors.tolist(), k=k)
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)