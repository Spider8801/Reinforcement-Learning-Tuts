 
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2d, MaxPooling2D, Activation, Flatten
class DQNAgent:
    def create_model(self):
        model = Sequential()