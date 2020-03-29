import numpy as np
import tensorflow as tf
print(tf.__version__)
# tf.logging.set_verbosity(tf.logging.INFO)

# This implementation is loosly based on the implementation of huib. Offcourse everything is understood and adaptions have been made to make it a normal NN.

def cnn_model_fn(features, labels, mode):
    """Model function for CNN."""
    # Input layer

    image1 = tf.cast(features["x"], tf.float32)

    input_layer = tf.reshape(image1, [-1,784]) # We have to reshape because the image is normaly formatted in 28x28.

    dense = tf.compat.v1.layers.dense(# We hope to find parts of the digit here.
        inputs=input_layer, # 784 input neurons go in here.
        units=300,
        activation=tf.nn.sigmoid
    )
    dense1 = tf.compat.v1.layers.dense( # We hope to find combination of above parts here.
        inputs=dense,
        units=300,
        activation=tf.nn.sigmoid
    )

    # Logits layer
    logits = tf.compat.v1.layers.dense(inputs=dense1, units=10) # 10 output nodes for 0-10 digits. 

    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add 'softmax_tensor' to the graph. It is used for PREDICT and by the 'logging_hook'
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate loss (for both TRAIN and EVAL modes)
    onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=10)
    loss = tf.compat.v1.losses.softmax_cross_entropy(onehot_labels=onehot_labels, logits=logits)

    # Configure the Training Op (for TRAIN)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.compat.v1.train.get_global_step()
        )
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.compat.v1.metrics.accuracy(
            labels=labels, predictions=predictions["classes"]
        )
    }
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops
    )

def main(unused_argv):
    # Load training and eval data
    mnist = tf.keras.datasets.mnist.load_data()
    train_data = mnist[0][0]
    train_labels = mnist[0][1]
    eval_data = mnist[1][0]
    eval_labels = mnist[1][1]

    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn,
        model_dir="/tmp/mnist_convnet_model"
    )

    # Set up logging for predictions
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.estimator.LoggingTensorHook(
        tensors=tensors_to_log, every_n_iter=50
    )

    # Train the model
    train_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=100, # We pass 100 images per weight update to tensorflow
        num_epochs=None,
        shuffle=True
    )
    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=10000,
        # hooks=[logging_hook]
    )

    # Evaluate the model and print results
    eval_input_fn = tf.compat.v1.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False
    )
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)


if __name__ == "__main__":
    tf.compat.v1.app.run()
