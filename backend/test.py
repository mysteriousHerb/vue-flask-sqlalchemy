import pickle
import hashlib
import os
import pickle


with open('known_descriptors\\9.jpg.pickle', 'rb') as handle:
    b = pickle.load(handle)
    print(b)



