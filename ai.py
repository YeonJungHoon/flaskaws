import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image
import os
from myproject import db
from myproject.models import Data
import shutil
import tensorflow as tf
from keras.models import Model

class Preprocessing():
    def __init__(self,image_length):
        self.image_length = image_length


    def image_resize(self):
        refine_path = 'static/refine_images'
        if os.path.isdir(refine_path):
            shutil.rmtree(refine_path)
            os.mkdir(refine_path)
        for i in os.listdir('static/img/'):
            path = 'static/img/{}'.format(i)
            img = Image.open(path)
            img_resize = img.resize((self.image_length,self.image_length))
            
            img_resize.save('static/refine_images/{}'.format(i))

    def img_to_array(self):
        num_file = len(os.listdir('static/refine_images'))
        var = np.zeros((self.image_length,self.image_length,num_file))
        for index , value in enumerate(os.listdir('static/refine_images')):
            path = 'static/refine_images/{}'.format(value)
            globals()['image_array' + str(index)] = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        
        for i in range(num_file):
            var[ :,:,i] = globals()['image_array' + str(i)]
        return var

    def make_y_train(self):
        y_train_data = Data.query.order_by(Data.id).all()
        y_train = []
        for datas in y_train_data:
            y_train.append(datas.data)
        
            

        return y_train
    def make_x_train(self, var):
        var = var / 255.0
        x_train = var.reshape(var.shape[2], var.shape[0],var.shape[1])
        return x_train
        

    def one_hot_encoding(self, y_train):
      y_train_set = set(tuple(y_train))
      #print(y_train_set)
      y_train = np.array(y_train)
      y_train_set_list = list(y_train_set)
      one_hot = np.zeros((len(y_train),len(y_train_set)))
      #print(one_hot.shape)
      for i in range(len(y_train)):
          for j in range(len(y_train_set)):
              if y_train[i] == y_train_set_list[j]:
                  one_hot[i,j] = 1
              else:
                  continue
      return one_hot

class Javis():

    def __init__(self,epoch, batch_size,x_train,y_train,image_length):
        self.epoch = epoch
        self.batch_size=batch_size
        self.x_train = x_train
        self.y_train = y_train
        self.image_length = image_length
        

    def LeNet(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(6, kernel_size = 5, strides = 1, activation ='tanh', input_shape = (self.image_length,self.image_length,1), padding= 'same'),
            tf.keras.layers.AveragePooling2D(pool_size=(2,2), strides =2),
            tf.keras.layers.Conv2D(16, kernel_size = 5, strides = 1, activation = 'tanh', padding = 'valid' ),
            tf.keras.layers.AveragePooling2D(pool_size=(2,2), strides =2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(120, activation = 'tanh'),
            tf.keras.layers.Dense(84, activation = 'tanh'),
            tf.keras.layers.Dense(self.y_train.shape[1] , activation = 'softmax')
        ])
        summary = model.summary()
        model.compile(loss='categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
        return model, summary

    def LeNet_train(self,model):
        model.fit(self.x_train, self.y_train, epochs = self.epoch, batch_size = self.batch_size)

    

class GAN():
    def __init__(self,image_length):
        self.image_length = image_length
    
    
    def Discriminator(self):
         discriminator = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(6, kernel_size = 5, strides = 1, activation ='tanh', input_shape = (self.image_length,self.image_length,1), padding= 'same'),
            tf.keras.layers.AveragePooling2D(pool_size=(2,2), strides =2),
            tf.keras.layers.Conv2D(16, kernel_size = 5, strides = 1, activation = 'tanh', padding = 'valid' ),
            tf.keras.layers.AveragePooling2D(pool_size=(2,2), strides =2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(120, activation = 'tanh'),
            tf.keras.layers.Dense(84, activation = 'tanh'),
            tf.keras.layers.Dense(24 , activation = 'tanh'),
            tf.keras.layers.Dense(1, activation = 'sigmoid')
            ])
         adam = tf.keras.optimizers.Adam(lr = 0.03, beta_1=  0.5)
         discriminator.compile(loss ='binary_crossentropy', optimizer =adam, metrics = ['accuracy'])
         return discriminator
    def make_noise(self):
        noise = tf.random.normal(shape = (self.image_length *4, self.image_length * 4), minval = 0, maxval = 1)
        return noise

    def Generator(self, noise):
        G = tf.keras.Sequential()
        G.add(tf.keras.layers.Dense(512, input_dim=self.image_length *4))
        G.add(tf.keras.activations.LeakyReLU(0.2))
        G.add(tf.keras.layers.Dense(128 * 7 * 7))
        G.add(tf.keras.activations.LeakyReLU(0.2))
        G.add(tf.keras.normalizations.BatchNormalization())
        G.add(tf.keras.layers.core.Reshape((128, 7, 7), input_shape=(128 * 7 * 7,)))
        G.add(tf.keras.layers.UpSampling2D(size=(2, 2)))
        G.add(tf.keras.layers.Conv2D(64, (5, 5), padding='same', activation='tanh'))
        G.add(tf.keras.layers.UpSampling2D(size=(2, 2)))
        G.add(tf.keras.layers.Conv2D(1, (5, 5), padding='same', activation='tanh'))

        adam = tf.keras.optimizers.Adam(lr=self.learning_rate, beta_1=0.5)
        G.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy'])
        return G
        
    
    def forward(self):
        G,D = self.Generator(), self.Discriminator()
        D.trainable = False
        gan = tf.keras.Sequential()
        gan.add(G)
        gan.add(D)
        adam = tf.keras.optimizers.Adam(lr = 0.05, beta_1 = 0.5)
        gan.compile(loss='binary_crossentropy', optimizer = adam, metrics = ['accuracy'])
        D.trainable = True
        return gan



       
        
        
        
    
                    
