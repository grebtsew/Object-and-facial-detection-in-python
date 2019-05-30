#! /usr/bin/env python

from __future__ import print_function

print( " Loading imports and setting init variables...")

import os
import sys

# This is a placeholder for a Google-internal import.

import tensorflow as tf
import numpy as np


import shutil
import os

learning_rate = 0.001

b = tf.Variable([.3], tf.float32, name='bias')
W = tf.Variable([-.3], tf.float32, name='weight')
x = tf.placeholder(tf.float32, name='X')
y = tf.placeholder(tf.float32, name='Y')

X_train      = [4.0, 0.0, 12.0]
Y_train      = [5.0, 9, -3]
linear_model = W*x + b   # y = W*x + b; 5= -1*4 + 9; 9=1*0 + 9;  -3 = -1*12 + 9

model_delta = tf.square(linear_model - y)
loss        = tf.reduce_sum(model_delta)
optimizer   = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
init        = tf.global_variables_initializer()

tf.app.flags.DEFINE_integer('training_iteration', 1000,
                            'number of training iterations.')
tf.app.flags.DEFINE_integer('model_version', 1, 'version number of the model.')
tf.app.flags.DEFINE_string('work_dir', '/tmp', 'Working directory.')
FLAGS = tf.app.flags.FLAGS



def main(_):
  # 'Saver' op to save and restore all the variables
  saver = tf.train.Saver()


  # Train model
  print('Training model...')
  with tf.Session() as sess:
      sess.run(init)
      for i in range(1000):
          feed_dict_batch = {x: X_train, y: Y_train}

          sess.run(optimizer, feed_dict=feed_dict_batch)
      W_value, b_value = sess.run([W, b])
      print(W_value)
      print(b_value)
      print('Done training!')

      # Export model
      # WARNING(break-tutorial-inline-code): The following code snippet is
      # in-lined in tutorials, please update tutorial documents accordingly
      # whenever code changes.
      export_path_base = "C:/Users/Daniel/Desktop/Tf_test/tmp2/"
      export_path_base2 = "C:/Users/Daniel/Desktop/Tf_test/tmp3/"
      #save_path = saver.save(sess, export_path_base)



      if os.path.exists(export_path_base) and os.path.isdir(export_path_base):
          shutil.rmtree(export_path_base)

      if os.path.exists(export_path_base2) and os.path.isdir(export_path_base2):
          shutil.rmtree(export_path_base2)


      export_path = os.path.join(
          tf.compat.as_bytes(export_path_base),
          tf.compat.as_bytes(str(FLAGS.model_version)))

      print('Exporting trained model to', export_path)
      builder = tf.saved_model.builder.SavedModelBuilder(export_path)

      x_info = tf.saved_model.utils.build_tensor_info(x)
      y_info = tf.saved_model.utils.build_tensor_info(y)
      W_info = tf.saved_model.utils.build_tensor_info(W)
      b_info = tf.saved_model.utils.build_tensor_info(b)

      #z = tf.placeholder( [x, y],tf.float32,  name='z')
      #q = tf.placeholder( [W, b], name='x')


      # Build the signature_def_map.
    #  classification_inputs = tf.saved_model.utils.build_tensor_info( x_info)
     # classification_outputs_scores = tf.saved_model.utils.build_tensor_info(b_info)

      classification_signature = (
          tf.saved_model.signature_def_utils.build_signature_def(
              inputs={
                  "x" :
                     x_info,
                     "y" :
                     y_info
              },
              outputs={
                  "w" :
                     W_info,
                     "b" :
                     b_info
              },
              method_name=tf.saved_model.signature_constants.CLASSIFY_METHOD_NAME))

      prediction_signature = ( tf.saved_model.signature_def_utils.build_signature_def(
               inputs={'X': x_info, 'Y': y_info},
               outputs={'W': W_info, 'B': b_info},
               method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME))

      export_path_base = "C:/Users/Daniel/Desktop/Tf_test/tmp3/"
      export_path = os.path.join(
           tf.compat.as_bytes(export_path_base),
           tf.compat.as_bytes(str(FLAGS.model_version)))

      builder = tf.saved_model.builder.SavedModelBuilder(export_path)
      builder.add_meta_graph_and_variables(
           sess, [tf.saved_model.tag_constants.SERVING],
           signature_def_map={
                'example':
                    prediction_signature,
                tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:
                    classification_signature,
           },


           legacy_init_op=tf.saved_model.main_op.main_op())
      builder.save()


      print('Done exporting!')
       # Testrun model
       # Test our new model
       # load model

      print("Our test program ")
      with tf.Session(graph=tf.Graph()) as sess:
          tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING],
           export_path_base2 + "1/")
          graph = tf.get_default_graph()

          for op in tf.get_default_graph().get_operations():
              print(str(op.name))
          X_ = graph.get_tensor_by_name("X:0")
          Y_ = graph.get_tensor_by_name("Y:0")
          weight_ = graph.get_tensor_by_name("weight:0")
          bias_ = graph.get_tensor_by_name("bias:0")

          w_, b_, x_, y_ = sess.run([weight_, bias_, X_,Y_],
          feed_dict={X_: [7, 5,23, 2,1], Y_: [1, 2, 3 , 4 , 1]} )


          print(w_ , b_, x_, y_)

if __name__ == '__main__':
    tf.app.run()
