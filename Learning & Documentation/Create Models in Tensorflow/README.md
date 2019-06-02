# Create Models in Tensorflow
This `README`-file contains a short tutorial of createing a tensorflow model. Code in this file is copied from files in this folder.

# Basics
Some common definitions will be described here.

What is Tensorflow*
* `Placeholder` ? - Variable used to store static data and take in data.
* `Proto` ? - Alot of google developed software uses proto, which are protocol buffers, google implementations.
* `Flags` ? - A wrapper for argparse, great use for metadata.
* `Variable` ? - Variable primary used to train data.

# Training your model
In this tutorial we won't look closer into building bigger neural networks. We rather focus on syntax and how to make the model run for demo examples. Here are some examples of training or just storing data in model.

This is how you get indata:

``python3

x = tf.placeholder(tf.float32, name='X')
y = tf.placeholder(tf.float32, name='Y')

# Float array
in_data =  tf.placeholder( tf.float32, shape=[10], name="IN_DATA")
```
Later you will be able to recieve outdata from placeholders and variables.

This is how you train a variable: (regression example)

``python3
b = tf.Variable([.3], tf.float32, name='bias')
W = tf.Variable([-.3], tf.float32, name='weight')

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
```

This is how you calculate something from Placeholder:

``python3

# Calculate Mean of array
mean = tf.reduce_mean(in_data, name="MEAN")

```

# Saving & Building
This is how you save your graph as checkpoints.

``python3

# Add ops to save and restore all the variables.
saver = tf.train.Saver()

save_path = saver.save(sess, "/tmp/model.ckpt")

```

This is how you save your model as `.pb`-files ready to be Served with `signature_def`:

``python3

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
```

# Building Servables (for Tensorflow Serving)
To make a model servable you need to add some metadata to the model to help the standard api.
It's helpful to understand proto request calls when doing this part.

An example of creating `signature_def` that calculate mean of incoming float32 array:
``python3

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
```

# How to run these example files

This is how can load and run model files:

``python3

#Our test program
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
```


This is how you would run a model that has been loaded into Tensorflow Serving standard:

``python3

from predict_client.prod_client import ProdClient

# in Send Proto Request Example
req_data = [{'in_tensor_name': 'inputs', 'in_tensor_dtype': 'DT_UINT8', 'data': img}]

client = ProdClient(host, model_name, model_version)

prediction = client.predict(req_data, request_timeout=10)
```

# Source and References
Main tutorial material and some code comes from tensorflow documentation:
https://www.tensorflow.org/guide

# Note
This short tutorial is for Tensorflow below version 2.0.
