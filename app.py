from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/uploaded'
CROPPED_FOLDER = 'static/images/cropped'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CROPPED_FOLDER'] = CROPPED_FOLDER

def crop_image(image_path, size, position):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    x, y = 0, 0

    if position == 'top_left':
        x, y = 0, 0
    elif position == 'top_center':
        x, y = (width - size) // 2, 0
    elif position == 'top_right':
        x, y = width - size, 0
    elif position == 'center_left':
        x, y = 0, (height - size) // 2
    elif position == 'center':
        x, y = (width - size) // 2, (height - size) // 2
    elif position == 'center_right':
        x, y = width - size, (height - size) // 2
    elif position == 'bottom_left':
        x, y = 0, height - size
    elif position == 'bottom_center':
        x, y = (width - size) // 2, height - size
    elif position == 'bottom_right':
        x, y = width - size, height - size

    cropped = image[y:y+size, x:x+size]
    cropped_filename = 'output.jpg'
    cropped_path = os.path.join(app.root_path, app.config['CROPPED_FOLDER'], cropped_filename)
    cv2.imwrite(cropped_path, cropped)
    return cropped_path


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return render_template('index.html', uploaded=True, filename=filename)
    return render_template('index.html')


@app.route('/crop/<filename>', methods=['GET', 'POST'])
def crop(filename):
    size = int(request.args.get('size'))
    position = request.args.get('position')
    image_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
    cropped_path = crop_image(image_path, size, position)
    return render_template('output.html', cropped_image=cropped_path)


if __name__ == '__main__':
    app.run(debug=True)
