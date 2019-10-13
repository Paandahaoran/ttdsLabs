import numpy as np
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer


ps = PorterStemmer()


a = 'NOT'

print (ps.stem(a))
