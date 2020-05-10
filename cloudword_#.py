#https://amueller.github.io/word_cloud/auto_examples/frequency.html?fbclid=IwAR1daWEyyo_zglYPiobS4pB6s-zOh8W8s68_SxdHERZxGG3hGbm35Np7ASk#sphx-glr-auto-examples-frequency-py

import multidict as multidict

import numpy as np

import os
import os.path 
import re
from PIL import Image
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json 

def makeImage(text, filename):
    alice_mask = np.array(Image.open("./hashtags/twitter_mask.jpg"))

    wc = WordCloud(background_color="white", max_words=1000, mask=alice_mask)
    # generate word cloud
    wc.generate_from_frequencies(text)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(filename.replace('.txt','.png'), dpi=600)
    plt.show()
    
# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

for dirpath, dirnames, filenames in os.walk("./hashtags"):
    for filename in [f for f in filenames if f.endswith(".txt")]:
        text = open(path.join(d, os.path.join(dirpath, filename)), encoding='utf-8')
        text = text.read()
        makeImage(json.loads(text), './hashtags/results/'+filename)


