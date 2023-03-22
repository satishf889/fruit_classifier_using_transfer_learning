from flask import Flask, request, render_template
import os
import numpy as np
import json
import base64
import io
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

app = Flask(__name__)


def predict_class(base64_decoded):
    img = image.load_img(io.BytesIO(base64_decoded), target_size=(224, 224))
    image_np = np.array(img)
    x = image_np
    x.shape
    x = 1.0*x/255
    # Adding the fouth dimension, for number of images
    x = np.expand_dims(x, axis=0)
    features = loaded_model.predict(x)
    # predicted_class = np.argmax(features)
    best_n = np.argsort(-features, axis=1)[:, :5]
    best_n = list(np.concatenate(best_n))
    result = {}
    for probability in best_n:
        result[classes_available[probability]
               ] = f'{round(features[0][probability]*100,2)}%'
    json_predicted_list = json.dumps(result, separators=(',', ':'))
    return json_predicted_list


def load_files(filename):
    with open(f"static//{filename}", 'r') as fl:
        classes_text_file = fl.read()
    classes_text_file = classes_text_file.replace(
        '\'', '').replace(',', '').replace(' ', '')
    return classes_text_file.split('\n')


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def fruit_predict():
    received_data = request.data
    json_data = json.loads(received_data)
    base64_image = json_data['text'].split(',')[1]
    base64_decoded = base64.b64decode(base64_image)
    predicted_list = predict_class(base64_decoded)
    return predicted_list


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    loaded_model = load_model("saved_models/fruitclassifier.h5")
    classes_available = load_files("classes_available.txt")
    app.run(host='0.0.0.0', port=port)
