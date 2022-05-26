import tensorflow as tf

def create_model():
  user_input = tf.keras.Input(shape=(4),)
  hotel_input = tf.keras.Input(shape=(14),)
  x = tf.keras.layers.Concatenate(axis=-1)([user_input, hotel_input])
  x = tf.keras.layers.Dense(128, activation="relu")(x)
  x = tf.keras.layers.Dense(64, activation="relu")(x)
  x = tf.keras.layers.Dense(32, activation="relu")(x)
  output = tf.keras.layers.Dense(units=1)(x)

  model = tf.keras.Model(inputs=[user_input, hotel_input], outputs=output)
  model.compile(optimizer="adam", loss="mean_absolute_error", metrics=["mean_absolute_error"])
  return model

model = tf.keras.models.load_model("./saved_model")