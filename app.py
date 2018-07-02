from flask import Flask, jsonify, request, send_file
import numpy as np
import tensorflow as tf
import model 
import io
from PIL import Image

app = Flask(__name__)
sess = tf.Session()
graph = model.load(sess)

@app.route('/tf', methods=['GET', 'POST'])
def tf():
  if request.method == 'GET':
    return 'Please POST this endpoint with your 28x28 MNIST png as file.'

  if 'file' not in request.files:
    return jsonify({
      'Error': '"file" in post request not found'
    })

  classify_file = request.files['file']

  if classify_file.filename.rsplit('.', 1) [1] != 'png':
    return jsonify({
      'Error': '"file" not in .png format'
    })

  img = Image.open(io.BytesIO(classify_file.read())).convert('L')
  img = img.resize((28, 28))
  img = np.array(img)
  img = np.expand_dims(img, axis=2)
  img = np.expand_dims(img, axis=0)
  response = model.predict(sess, graph, img)

  return jsonify(response.tolist()[0])