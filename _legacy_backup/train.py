import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import os

img_height, img_width = 48, 48
batch_size = 32
num_classes = 6
epochs = 50

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_generator = train_datagen.flow_from_directory(
    'data/train',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode='grayscale',
    class_mode='categorical'
)

input_layer = Input(shape=(img_height, img_width, 1))
conv_layer = Conv2D(3, (1, 1), padding='same')(input_layer)

base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights=None,
    alpha=0.35
)

x = base_model(conv_layer)
x = GlobalAveragePooling2D()(x)
output_layer = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=input_layer, outputs=output_layer)

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

early_stopping = EarlyStopping(
    monitor='loss',
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='loss',
    factor=0.5,
    patience=3,
    min_lr=1e-7
)

history = model.fit(
    train_generator,
    epochs=epochs,
    callbacks=[early_stopping, reduce_lr]
)

model.save('models/emotion_model.h5')
print("Model saved to models/emotion_model.h5")
