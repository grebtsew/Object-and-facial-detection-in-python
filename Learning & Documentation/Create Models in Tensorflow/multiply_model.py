'''
This model multiply values on placeholder X & Y to Variable Z.
Test this model!
'''

print( " Loading imports and setting init variables...")

import sys
import tensorflow as tf
import numpy as np
import shutil
import os

x = tf.placeholder(tf.float32, name="X")
y = tf.placeholder(tf.float32, name="Y")
z = tf.multiply(x, y, name="Z")

tf.app.flags.DEFINE_integer('training_iteration', 1000,
                            'number of training iterations.')
tf.app.flags.DEFINE_integer('model_version', 1, 'version number of the model.')
tf.app.flags.DEFINE_string('work_dir', '/tmp', 'Working directory.')
FLAGS = tf.app.flags.FLAGS

init = tf.global_variables_initializer()



def main():
    export_path_base = "C:/Users/Daniel/Desktop/Tf_test/tmp2/"
    export_path_base2 = "C:/Users/Daniel/Desktop/Tf_test/tmp3/"

    with tf.Session() as sess:
        sess.run(init)

        # create model

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
        z_info = tf.saved_model.utils.build_tensor_info(z)


        classification_signature = (
              tf.saved_model.signature_def_utils.build_signature_def(
                  inputs={
                      "X" :
                         x_info,
                         "Y" :
                         y_info
                  },
                  outputs={
                         "Z" :
                         z_info
                  },
                  method_name=tf.saved_model.signature_constants.CLASSIFY_METHOD_NAME))

        prediction_signature = ( tf.saved_model.signature_def_utils.build_signature_def(
                   inputs={'X': x_info, 'Y': y_info},
                   outputs={'Z': z_info},
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



if __name__ == '__main__':
    main()

       # Testrun model
       # Test our new model
       # load model

    export_path_base2 = "C:/Users/Daniel/Desktop/Tf_test/tmp3/"

    print("Our test program ")
    with tf.Session(graph=tf.Graph()) as sess:
      tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING],
       export_path_base2 + "1/")
      graph = tf.get_default_graph()

      for op in tf.get_default_graph().get_operations():
          print(str(op.name))
      X_ = graph.get_tensor_by_name("X:0")
      Y_ = graph.get_tensor_by_name("Y:0")
      z_ = graph.get_tensor_by_name("Z:0")

      z_ = sess.run(z_,
      feed_dict={X_: [7, 5,23, 2,1], Y_: [1, 2, 3 , 4 , 1]} )

      print(z_)
