# Create Models in Tensorflow


# Basics
Some common definitions will be described here.

What is Tensorflow*
* Placeholder? -
* Proto? -
* Flags? -
* Variable? -

# Training your model
In this tutorial we won't look closer into building bigger neural networks. We rather focus on syntax and how to make the model run for demo examples. Here are some examples of training or just storing data in model.


This is how you get indata:

```python3

```
Later you will be able to recieve outdata from placeholders and variables.

This is how you train a varible:

```python3

```


This is how you calculate something from Placeholder:

```python3

```



# Saving & Building
This is how you save your graph as checkpoints:

```python3

```

This is how you save your model as .pb-files:

```python3

```


# Building Servables (for Tensorflow Serving)
To make a model servable you need to add some metadata to the model to help the standard api.
It's helpful to understand proto request calls when doing this part.

What you need to add is described in this code-snippet:


# How to run these example files

This is how can load and run model files:

```python3

```


This is how you run a model that has been loaded into Tensorflow Serving standard:

```python3

```


# Source and References


# Note
This short tutorial is for Tensorflow below version 2.0.
