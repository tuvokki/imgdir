import tensorflow as tf

from train_mos import create_empty_model

devices = tf.config.list_physical_devices()
print(devices)
tf.debugging.set_log_device_placement(True)
a=tf.random.normal([100,100])
b=tf.random.normal([100,100])
c = a*b

create_empty_model()