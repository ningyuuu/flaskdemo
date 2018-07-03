import tensorflow as tf
import math
import os
from tensorflow.examples.tutorials.mnist import input_data as mnist_data

# input X: 28x28 grayscale images, the first dimension (None) will index the images in the mini-batch
def build_graph():
  x = tf.placeholder(tf.float32, [None, 28, 28, 1], name='x')
  y_ = tf.placeholder(tf.float32, [None, 10], name='y_')
  W = tf.Variable(tf.zeros([784, 10]))
  b = tf.Variable(tf.zeros([10]))
  xx = tf.reshape(x, [-1, 784])
  y = tf.nn.softmax(tf.matmul(xx, W) + b)

  cross_entropy = -tf.reduce_mean(y_ * tf.log(y)) * 1000.0 
  train_step = tf.train.GradientDescentOptimizer(0.005, name='GradientDescent').minimize(cross_entropy)
  classification = tf.argmax(y, 1, name='classification')

  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

  return tf.get_default_graph()

def build_better_graph():
  pass

def build_better_better_graph():
  pass

def train(sess, graph, iters=10000):
  mnist = mnist_data.read_data_sets("data", one_hot=True, reshape=False, validation_size=0)

  x = graph.get_tensor_by_name('x:0')
  y_ = graph.get_tensor_by_name('y_:0')
  train_step = graph.get_operation_by_name('GradientDescent')
  sess.run(tf.global_variables_initializer())

  for r in range(iters):
    if (r % 200) == 0:
      print('Train:', r)
    batch_X, batch_Y = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_X, y_: batch_Y})

def predict(sess, graph, image):
  x = graph.get_tensor_by_name('x:0')
  classification = graph.get_tensor_by_name('classification:0')
  return sess.run(classification, feed_dict={x: image})

def save(sess, path_name='model', model_name='main'):
  os.makedirs(os.path.join(os.path.dirname(os.path.realpath(__file__)), path_name, model_name), exist_ok=True)
  saver = tf.train.Saver()
  saver.save(sess, os.path.join(os.path.dirname(os.path.realpath(__file__)), path_name, model_name, 'model'))

def load(sess, path_name='model', model_name='main'):
  print(os.path.join(os.path.dirname(os.path.realpath(__file__)), path_name, model_name, 'model.meta'))
  saver = tf.train.import_meta_graph(os.path.join(os.path.dirname(os.path.realpath(__file__)), path_name, model_name, 'model.meta'))
  saver.restore(sess, tf.train.latest_checkpoint(os.path.join(os.path.dirname(os.path.realpath(__file__)), path_name, model_name)))
  return tf.get_default_graph()

def test(sess, graph):
  x = graph.get_tensor_by_name('x:0')
  y_ = graph.get_tensor_by_name('y_:0')
  accuracy = graph.get_tensor_by_name('accuracy:0')
  return sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})

if __name__ == '__main__':
  sess = tf.Session()
  # graph = load(sess)
  graph = build_graph()
  train(sess, graph)
  print('test', test(sess, graph))
  save(sess)