# -*- coding: utf-8 -*-
"""Neural network for image classification.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mHs259KOHYbxSbFqywSJAk15gibT6Us1

# Approach 1 : Extract All pixels

##Import Libraries
"""

import cv2
import numpy as np
import os  #to have access to resources regarding the operational system
import zipfile
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
import tensorflow as tf
import pandas as pd
import seaborn as sns
tf.__version__

"""## Extracting pixels from all the images"""

from google.colab import drive
drive.mount('/content/drive')

path = '/content/drive/MyDrive/Computer Vision Masterclass/Datasets/homer_bart_1.zip'
zip_object = zipfile.ZipFile(file=path, mode='r') #r means read
zip_object.extractall('./')
zip_object.close()

directory = '/content/homer_bart_1'
files = [os.path.join(directory, file) for file in os.listdir(directory)]

for file in files:
  print(file)

type(files)

height, width = 128,128

images = [] #store pixels of the images
classes = [] # store class of each image

128*128*3 #colored image -> nb of neurons in input layer
128* 128 #grayscale image -> nb of neurons in input layer

for image_path in files:
  #print(image_path)
  try:
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]
  except:
    continue

  image = cv2.resize(image, (width, height))
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  cv2_imshow(image)

  image = image.ravel()
  print(image.shape)

  images.append(image)

  image_name = os.path.basename(os.path.normpath(image_path))
  if image_name.startswith('b'):
    class_name = 0
  else:
    class_name = 1

  classes.append(class_name)
  print(class_name)

image.shape

images

image_name

classes

classes[-1]

type(images), type(classes)

#we need images and classes in numpy format to send them to the nerual network
X = np.asarray(images)
y = np.asarray(classes)

type(X), type(y)

X.shape

y.shape

y

X[0].reshape(width, height).shape # we need to convert the vector to a matrix to visualize it
cv2_imshow(X[0].reshape(width, height))

cv2_imshow(X[20].reshape(width, height))

sns.countplot(y)

# Set the labels for better readability
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Count of 0s and 1s')

# Show the plot
plt.show()

plt.hist(y, bins=[-0.5, 0.5, 1.5], edgecolor='black', rwidth=0.8)

# Set labels and title
plt.xticks([0, 1])  # Set x-ticks to only 0 and 1
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Histogram of 0s and 1s')

# Show the plot
plt.show()

np.unique(y, return_counts=True)

"""## Normalizing the data"""

X[0].max(), X[0].min() # 255 white color, 0 is black

# normalize the data to let the process be faster ( because it performs matrix multiplication)
# another problem is that if you send these values in this big scale to neural network, the results will not be so good

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

X[0].max(), X[0].min()

X[1]

"""## Train and test"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1) #random state means havinf the same images in the variable

X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""## Build and Train neural netwrok"""

(16384+2)/2

network1 = tf.keras.models.Sequential() #sequence  of layers
# dense neural network is when one neuron from one layer is connected to the other neurons of the next layer
#16384 (input layer) -> 8193 ( hidder layer) -- > 8193  --> 1 (binary classification problem)
network1.add(tf.keras.layers.Dense(input_shape=(16384, ), units=8193, activation='relu'))
network1.add(tf.keras.layers.Dense(units=8193, activation='relu'))
network1.add(tf.keras.layers.Dense(units=1, activation='sigmoid')) #binary classification problem

network1.summary()

network1.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])

history = network1.fit(x=X_train, y=y_train, epochs=50) #adjust weight

"""## Evaluating the neural network"""

history.history.keys()

plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')

plt.plot(history.history['accuracy'])

X_test

X_test.shape

predictions = network1.predict(X_test)

predictions #sigmoid that returns a probabily close to 0 : bart / close to 1 homer

#0 FALSE - BART
#1 TRUE - HOMER
predictions = (predictions > 0.5)
predictions

y_test

predictions.shape, y_test.shape

from sklearn.metrics import accuracy_score
accuracy_score(y_test, predictions)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, predictions)
cm

# sns.heatmap(cm)
sns.heatmap(cm, annot=True)

from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))
# can correctly identify 0.76 of bart images, and 0.43 homer images
# when we identify these bart images it is correct 68% of the times
# when we identify these gomer images it is correct 53% of the times

"""## Saving and loading the network"""

model_json = network1.to_json()
with open('network1.json', 'w') as json_file:
  json_file.write(model_json)

from keras.models import save_model
network1_saved = save_model(network1, 'weights1.hdf5')

with open('network1.json', 'r') as json_file:
  json_saved_model = json_file.read()
json_saved_model

network1_loaded = tf.keras.models.model_from_json(json_saved_model)
network1_loaded.load_weights('weights1.hdf5')

network1_loaded.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])

network1_loaded.summary()

"""## Classifying one single image"""

test_image = X_test[0]
cv2_imshow(X_test[0].reshape(width, height)) #now we need to rescale the image

test_image

test_image = scaler.inverse_transform(test_image.reshape(1, -1))
test_image

cv2_imshow(test_image.reshape(width, height))

network1_loaded.predict(test_image)

network1_loaded.predict(test_image)[0][0]

if network1_loaded.predict(test_image)[0][0] < 0.5:
  print('Bart')
else:
  print('Homer')

test_image = X_test[33]
test_image = scaler.inverse_transform(test_image.reshape(1, -1))
test_image

cv2_imshow(test_image.reshape(width, height))

if network1_loaded.predict(test_image)[0][0] < 0.5:
  print('Bart')
else:
  print('Homer')

"""# Approach 2 :  feature extrcation"""

files = [os.path.join(directory, file) for file in os.listdir(directory)]
print(files)

export = 'mouth, pants, shoes, tshirt, shorts, sneakers, class\n'

show_images = True
features = []

100*200

(2000/20000)*100 #in 10 % of the images we have brown color

for image_path in files:
  #print(image_path)
  try:
    original_image = cv2.imread(image_path)
    (H, W) = original_image.shape[:2]
  except:
    continue

  image = original_image.copy()
  image_features = []
  mouth = pants = shoes = 0
  tshirt = shorts = sneakers = 0

  image_name = os.path.basename(os.path.normpath(image_path))

  if image_name.startswith('b'):
    class_name = 0
  else:
    class_name = 1

  for height in range(0, H):
    for width in range(0, W):
      blue = image.item(height, width, 0)
      green = image.item(height, width, 1)
      red = image.item(height, width, 2)

      # Homer - brown mouth
      if (blue >= 95 and blue <= 140 and green >= 160 and green <= 185 and red >= 175 and red <= 200):
        image[height, width] = [0, 255, 255]
        mouth += 1

      # Homer - blue pants
      if (blue >= 150 and blue <= 180 and green >= 98 and green <= 120 and red >= 0 and red <= 90):
        image[height, width] = [0, 255, 255]
        pants += 1

      # Homer - gray shoes
      #access the half bottom of the image
      if height > (H / 2):
        if (blue >= 25 and blue <= 45 and green >= 25 and green <= 45 and red >= 25 and red <= 45):
          image[height, width] = [0, 255, 255]
          shoes += 1

      # Bart - orange t-shirt
      if (blue >= 11 and blue <= 22 and green >= 85 and green <= 105 and red >= 240 and red <= 255):
        image[height, width] = [0, 255, 128]
        tshirt += 1

      # Bart - blue shorts
      if (blue >= 125 and blue <= 170 and green >= 0 and green <= 12 and red >= 0 and red <= 20):
        image[height, width] = [0, 255, 128]
        shorts += 1

      # Bart - blue sneakers
      #access the half bottom of the image
      if height > (H / 2):
        if (blue >= 125 and blue <= 170 and green >= 0 and green <= 12 and red >= 0 and red <= 20):
          image[height, width] = [0, 255, 128]
          sneakers += 1

  mouth = round((mouth / (H * W)) * 100, 9)
  pants = round((pants / (H * W)) * 100, 9)
  shoes = round((shoes / (H * W)) * 100, 9)
  tshirt = round((tshirt / (H * W)) * 100, 9)
  shorts = round((shorts / (H * W)) * 100, 9)
  sneakers = round((sneakers / (H * W)) * 100, 9)

  image_features.append(mouth)
  image_features.append(pants)
  image_features.append(shoes)
  image_features.append(tshirt)
  image_features.append(shorts)
  image_features.append(sneakers)
  image_features.append(class_name)

  features.append(image_features)

  #print('Homer mouth: %s - Homer pants: %s - Homer shoes: %s' % (image_features[0], image_features[1], image_features[2]))
  #print('Bart t-shirt: %s - Bart shorts: %s - Bart sneakers: %s' % (image_features[3], image_features[4], image_features[5]))

  f = (",".join([str(item) for item in image_features]))
  export += f + '\n'

  if show_images == True:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    fig, im = plt.subplots(1, 2)
    im[0].axis('off')
    im[0].imshow(original_image)
    im[1].axis('off')
    im[1].imshow(image)
    plt.show()

image_features

features

export

with open('features.csv', 'w') as f:
  for l in export:
    f.write(l)
f.closed

dataset = pd.read_csv('features.csv')
dataset.head()

"""## Train & test sets"""

X = dataset.iloc[:, :-1].values # all rows, all columns except the last one
y = dataset.iloc[:, -1].values

X, y

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""## Build and Train the neural network"""

(6+2)/2

network2 = tf.keras.models.Sequential()
#6 -> 4->4 ->4 ->1
network2.add(tf.keras.layers.Dense(input_shape =(6,),units=4, activation='relu'))
network2.add(tf.keras.layers.Dense(units=4, activation='relu'))
network2.add(tf.keras.layers.Dense(units=4, activation='relu'))
network2.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

network2.summary()

network2.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])

history = network2.fit(x=X_train, y=y_train, epochs=50)

"""## Evaluating neural netwrok"""

history.history.keys()

plt.plot(history.history['loss'])
plt.title('model loss')

plt.plot(history.history['accuracy'])

X_test.shape

predictions = network2.predict(X_test)

predictions

predictions = (predictions > 0.5)
predictions

y_test

from sklearn.metrics import accuracy_score
accuracy_score(y_test, predictions)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, predictions)
cm

plt.figure(figsize=(7, 5))
sns.heatmap(cm, annot=True)

from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))

"""## Saving, loading and classifying one single image"""

model_json = network2.to_json()
with open('network2.json', 'w') as json_file:
  json_file.write(model_json)

from keras.models import save_model
network2_saved = save_model(network2, 'weights2.hdf5')

with open('network2.json', 'r') as json_file:
  json_saved_model = json_file.read()
json_saved_model

network2_loaded = tf.keras.models.model_from_json(json_saved_model)
network2_loaded.load_weights('weights2.hdf5')
network2.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])

network2_loaded.summary()

test_image = X_test[33]
test_image

test_image.shape

test_image = test_image.reshape(1, -1)
test_image.shape

network2_loaded.predict(test_image)

if network2_loaded.predict(test_image)[0][0] < 0.5:
  print('Bart')
else:
  print('Homer')

"""# Cat and Dogs Classification"""

path = '/content/drive/MyDrive/Computer Vision Masterclass/Datasets/cat_dog_1.zip'
zip_object = zipfile.ZipFile(file=path, mode='r') #r means read
zip_object.extractall('./')
zip_object.close()

directory_train = '/content/cat_dog_1/train'
directory_test = '/content/cat_dog_1/test'
files_train = [os.path.join(directory_train, f) for f in sorted(os.listdir(directory_train))]
files_test = [os.path.join(directory_test, f) for f in sorted(os.listdir(directory_test))]

height, width = 128,128

"""## Train"""

images = []
classes = []
for image_path in files_train:
  #print(image_path)
  try:
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]
  except:
    continue

  image = cv2.resize(image, (width, height))
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  cv2_imshow(image)

  image = image.ravel()
  print(image.shape)

  images.append(image)

  image_name = os.path.basename(os.path.normpath(image_path))
  if image_name.startswith('c'):
    class_name = 0
  else:
    class_name = 1

  classes.append(class_name)
  print(class_name)

#we need images and classes in numpy format to send them to the nerual network
X = np.asarray(images)
y = np.asarray(classes)

X[0].reshape(width, height).shape # we need to convert the vector to a matrix to visualize it
cv2_imshow(X[0].reshape(width, height))

plt.hist(y, bins=[-0.5, 0.5, 1.5], edgecolor='black', rwidth=0.8)

# Set labels and title
plt.xticks([0, 1])  # Set x-ticks to only 0 and 1
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Histogram of 0s and 1s')

# Show the plot
plt.show()

images = []
classes = []
for image_path in files_test:
  #print(image_path)
  try:
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]
  except:
    continue

  image = cv2.resize(image, (width, height))
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  cv2_imshow(image)

  image = image.ravel()
  print(image.shape)

  images.append(image)

  image_name = os.path.basename(os.path.normpath(image_path))
  if image_name.startswith('c'):
    class_name = 0
  else:
    class_name = 1

  classes.append(class_name)
  print(class_name)

X_test = np.asarray(images)
y_test = np.asarray(classes)

plt.hist(y_test, bins=[-0.5, 0.5, 1.5], edgecolor='black', rwidth=0.8)

# Set labels and title
plt.xticks([0, 1])  # Set x-ticks to only 0 and 1
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Histogram of 0s and 1s')

# Show the plot
plt.show()

"""## Normalizing the data"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X= scaler.fit_transform(X)
X_test = scaler.transform(X_test)

"""## Build and train the neural network"""

# 16384 -> 8193 -> 8193 -> 1
network1 = tf.keras.models.Sequential()
network1.add(tf.keras.layers.Dense(input_shape=(16384,), units=8193, activation='relu'))
network1.add(tf.keras.layers.Dense(units=8193, activation = 'relu'))
network1.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

network1.summary()

network1.compile(optimizer='Adam', loss='binary_crossentropy', metrics = ['accuracy'])

history = network1.fit(X, y, epochs=10)

"""## Evaluating the neural network"""

plt.plot(history.history['loss']);

plt.plot(history.history['accuracy']);

predictions = network1.predict(X_test)
predictions

predictions = (predictions > 0.5)
predictions

from sklearn.metrics import accuracy_score
accuracy_score(y_test, predictions)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, predictions)
cm

sns.heatmap(cm, annot=True);

from sklearn.metrics import classification_report
print(classification_report(y_test, predictions))

