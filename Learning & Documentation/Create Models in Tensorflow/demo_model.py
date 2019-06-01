'''
This model multiply values on placeholder X & Y to Variable Z.
Test this model!
'''
import json

print( " Loading imports and setting init variables...")

import sys
import tensorflow as tf
import numpy as np
import shutil
import os

test = '[{"name":"rcnn","data":1}]'

#in_json = tf.placeholder( tf.string, name="IN_JSON")
in_data =  tf.placeholder( tf.float32, shape=[10], name="IN_DATA")

'''
def get_json(instr):
    val_list = []

    d = json.loads(instr.numpy().decode("utf-8"))
    for data in d:
        for p in data["parameters"]:
            val_list.append(float(p[0]["value"]))
    return np.array(val_list, dtype='f')
'''

#[parsed] = tf.py_function(get_json, [in_json], [tf.float32])


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

        mean = tf.reduce_mean(in_data, name="MEAN")

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

        x_info = tf.saved_model.utils.build_tensor_info(in_data)
        z_info = tf.saved_model.utils.build_tensor_info(mean)

        classification_signature = (
              tf.saved_model.signature_def_utils.build_signature_def(
                  inputs={
                      "IN_DATA" :
                         x_info
                  },
                  outputs={
                         "MEAN" :
                         z_info
                  },
                  method_name=tf.saved_model.signature_constants.CLASSIFY_METHOD_NAME))

        prediction_signature = ( tf.saved_model.signature_def_utils.build_signature_def(
                   inputs={'IN_DATA': x_info},
                   outputs={'MEAN': z_info},
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
      X_ = graph.get_tensor_by_name("IN_DATA:0")

      z_ = graph.get_tensor_by_name("MEAN:0")

      z_ = sess.run(z_,
      feed_dict={X_: [10,20,30,40,50,60,70,80,90,100]} )

      print(z_)
