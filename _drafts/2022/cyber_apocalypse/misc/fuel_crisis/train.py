import tensorflow as tf
import numpy as np

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
y_test_orig = y_test.copy()
for i in range(len(y_train)):
    if y_train[i] == 2:
        y_train[i] = 8

for i in range(len(y_test)):
    if y_test[i] == 2:
        y_test[i] = 8

x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(10)
])
model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)

model.fit(
    x = x_train,
    y = y_train,
    epochs=6,
    validation_data=(x_test, y_test),
)


