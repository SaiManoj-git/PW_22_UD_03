import os
from flask import Flask, render_template
from flask.json import JSONEncoder
from flask_cors import CORS
from flask import Flask, redirect, jsonify, request, url_for, render_template, flash
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
import base64


from bson import json_util, ObjectId
from datetime import datetime, timedelta

# from app.api.users import

allowed_exts = {'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'}


def check_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app():
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'build')

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                )

    CORS(app)
    app.json_encoder = MongoJsonEncoder

    # Register apis here
    # app.register_blueprint(blueprint_name)

    # a simple page that says hello
    '''@app.route('/')
    def hello():
        return render_template("upload_image.html")
    '''

    @app.route('/uploads/<filename>')
    def send_uploaded_file(filename=''):
        from flask import send_from_directory
        return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        if request.method == 'POST':
            if 'file' not in request.files:
                print('No file attached in request')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                print('No file selected')
                return redirect(request.url)
            if file and check_allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                img = Image.open(file.stream)
                with BytesIO() as buf:
                    img.save(buf, 'jpeg')
                    image_bytes = buf.getvalue()
                encoded_string = base64.b64encode(image_bytes).decode()

            # img-image image in Pil Image form
            # pass img to API
            print(img)

            return render_template('upload_image.html', img_data=encoded_string), 200
        else:
            return render_template('upload_image.html', img_data=""), 200

    return app
