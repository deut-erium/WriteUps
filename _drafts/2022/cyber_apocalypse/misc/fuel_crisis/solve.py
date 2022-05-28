mport tensorflow as tf
model = tf.keras.models.load_model('application/models/model.h5')
weights = model.get_weights()
weights[-1][2] = -100 # bias for 2 very very negative
model.set_weights(weights)
model.save("model2.h5")
# HTB{4ttack1ng_l4st_l4yers}
