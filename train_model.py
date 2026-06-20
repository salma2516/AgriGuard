from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

train = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_data = train.flow_from_directory(
    "dataset",
    target_size=(128,128),
    batch_size=32,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_data = train.flow_from_directory(
    "dataset",
    target_size=(128,128),
    batch_size=32,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

print("\nClasses Found:")
print(train_data.class_indices)

num_classes = len(train_data.class_indices)

model = Sequential()

model.add(Conv2D(32,(3,3),activation='relu',
                 input_shape=(128,128,3)))
model.add(MaxPooling2D())

model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D())

model.add(Conv2D(128,(3,3),activation='relu'))
model.add(MaxPooling2D())

model.add(Flatten())

model.add(Dense(256,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(num_classes,activation='softmax'))

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)

model.save("model/crop_model.h5")

print("\nModel Saved Successfully!")