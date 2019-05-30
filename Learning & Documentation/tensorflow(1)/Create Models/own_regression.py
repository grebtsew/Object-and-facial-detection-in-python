import numpy as np
import tensorflow as tf
import shutil
import os

STEPS = 1000
PRICE_NORM_FACTOR = 1000

b = tf.Variable([.3], tf.float32, name='bias')
W = tf.Variable([-.3], tf.float32, name='weight')
x = tf.placeholder(tf.float32, name='X')

test = [5.0, 9, -3]

feature_columns = [
    tf.feature_column.numeric_column(key="x")
]

def create_dataset():
    dataset1 = tf.data.Dataset.from_tensor_slices({"x": tf.random_uniform([4, 10])})
    #print(dataset1.output_types)  # ==> "tf.float32"
    #print(dataset1.output_shapes)  # ==> "(10,)"
    return dataset1

def main(argv):
    train = create_dataset()
    input = train.shuffle(1000).batch(128).repeat().make_initializable_iterator().get_next()
    print(train )

    # Build the Estimator.
    model = tf.estimator.LinearRegressor(feature_columns=feature_columns)

    # Train the model.
    # By default, the Estimators log output every 100 steps.
    model.train(input_fn=input, steps=1000)

    # Evaluate how the model performs on data it has not yet seen.
    eval_result = model.evaluate(input_fn=input)

    print (eval_result)

    print("got dataset")


if __name__ == "__main__":
  # The Estimator periodically generates "INFO" logs; make these logs visible.

  tf.app.run(main=main)
