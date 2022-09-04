import os
from flask import Flask, render_template
from flask.json import JSONEncoder
from flask_cors import CORS
from flask import Flask, redirect, jsonify, request, url_for, render_template, flash
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image
import base64
import numpy as np
from matplotlib import cm

import tensorflow as tf
from tensorflow import keras


from bson import json_util, ObjectId
from datetime import datetime, timedelta

from app.display_image import inpImage

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


def deblur_image(img):

    img_inp=img.reshape(1,128,128,3)
    # result = autoencoder.predict(img_inp)
    # imgArray = np.asarray(img)
    # print(imgArray)
    # print(imgArray.shape)
    model = tf.keras.models.load_model(r'app\best_models\try4')
    model.summary()

    result = model.predict(img_inp)
    
    # inpImage(result)        # BACKUP TO CHECK
    
    
    # output = np.transpose(result[[2, 1, 0], :, :], (1, 2, 0)) * 255.0
    # output = output.round().squeeze()
    # output = Image.fromarray(output.astype(np.uint8))

    
    result = (result.reshape(128,128,3) * 255).astype(np.uint8)
    img = Image.fromarray(result, mode='RGB').convert('RGB')
    print("Image size",img.size)
    return img


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
        print("here",app.config["IMAGE_UPLOADS"], filename)
        return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

    # @app.route("/", methods=['GET', 'POST'])
    # def hello():
    #     if request.method == 'POST':
    #         if 'file' not in request.files:
    #             print('No file attached in request')
    #             return redirect(request.url)
    #         file = request.files['file']
    #         if file.filename == '':
    #             print('No file selected')
    #             return redirect(request.url)
    #         if file and check_allowed_file(file.filename):
    #             filename = secure_filename(file.filename)
    #             print(filename)
    #             # preprocess
    #             image = tf.keras.preprocessing.image.load_img(filename, target_size=(128,128))
    #             image = tf.keras.preprocessing.image.img_to_array(image).astype('float32') / 255
    #             final_img = deblur_image(image)
                
    #             # final_img = Image.open(file.stream)
    #             with BytesIO() as buf:
    #                 final_img.save(buf, 'jpeg')
    #                 image_bytes = buf.getvalue()
    #             encoded_string = base64.b64encode(image_bytes).decode()
    #         # img-image image in Pil Image form
    #         # pass img to API
    #         # img = img.resize((128, 128))
    #         # final_img = deblur_image(img)
    #         # print(final_img)

    #         return render_template('upload_image.html', img_data=encoded_string), 200
    #     else:
    #         white_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg=="
    #         return render_template('upload_image.html', img_data=white_image), 200

    @app.route('/', methods=['GET', 'POST'])
    def upload_image():
        if request.method == "POST":
            if request.files:
                image = request.files["image"]
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                #  preprocess
                img = tf.keras.preprocessing.image.load_img(os.path.join(app.config["IMAGE_UPLOADS"], image.filename), target_size=(128,128))
                img = tf.keras.preprocessing.image.img_to_array(img).astype('float32') / 255
                final_img = deblur_image(img)

                final_img.save(os.path.join(app.config["IMAGE_UPLOADS"], "result.png"), quality='500')

                return render_template("upload_image.html", uploaded_image="result.png")
        
        return render_template("upload_image.html")



    return app
