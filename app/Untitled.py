
# coding: utf-8


import argparse
# Define the parser
parser = argparse.ArgumentParser(description='Short sample app')
# Declare an argument (`--algo`), telling that the corresponding value should be stored in the `algo` field, and using a default value if the argument isn't given
parser.add_argument('--words', action="store", dest='words', default=500)
parser.add_argument('--clusters', action="store", dest='clusters', default=10)
# Now, parse the command line arguments and store the values in the `args` variable
args = parser.parse_args()
# Individual arguments can be accessed as attributes...
# print(args.algo)

#print(type(int(args.clusters)))
#print(type(args.words))


# In[1]:


import gensim
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format('/home/ubuntu/imdb/models/model.wv')
# model = gensim.models.Word2Vec.load('/home/stlk/Desktop/pwc/tsne_clust/model.bin')
word_vectors = KeyedVectors.load_word2vec_format('/home/ubuntu/imdb/models/model.wv', 
                                                 encoding='utf8', binary = False)
# word_vectors =  KeyedVectors.load_word2vec_format('/home/stlk/Desktop/pwc/tsne_clust/model.bin', 
 #                                          binary = True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# get_ipython().run_line_magic('matplotlib', 'inline')


vocab = list(model.wv.vocab)
# vocab


# In[2]:


import argparse
import logging
import time
import codecs
from sklearn.cluster import KMeans
import numpy as np
import sklearn
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARNING)


def km(model, clusters):
    
    #model = model
    # clusters = 10
    
    start = time.time()
    print("Load word2vec model ... ", end="", flush=True)
    w2v_model = model
    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
    word_vectors = w2v_model.wv.syn0
    n_words = word_vectors.shape[0]
    vec_size = word_vectors.shape[1]
    print("#words = {0}, vector size = {1}".format(n_words, vec_size))

    start = time.time()
    print("Compute clustering ... ", end="", flush=True)
    kmeans = KMeans(n_clusters = clusters, n_jobs=-1, random_state=0)
    idx = kmeans.fit_predict(word_vectors)
    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)

    start = time.time()
    print("Generate output file ... ", end="", flush=True)
    word_centroid_list = list(zip(w2v_model.wv.index2word, idx))
    word_centroid_list_sort = sorted(word_centroid_list, key=lambda el: el[1], reverse=False)
    
            # with codecs.open(file_name, "r",encoding='utf-8', errors='ignore') as fdata:
        
    
    file_out = open("output_cluster", "w", encoding='utf-8', errors='ignore')
    file_out.write("/home/ruser/imdb/data/n")
    
    
    clst = pd.DataFrame()
    lst = list()
    lst_centr = list()
    # lst.append(2)
    for word_centroid in word_centroid_list_sort:
        word_centroid_list_sort[0]
        line = word_centroid[0] + '\t' + str(word_centroid[1]) + '\n'
        lst.append(word_centroid[0]) 
        lst_centr.append(str(word_centroid[1]))        
        file_out.write(line)
    file_out.close()
    
    clst['words'] = lst
    clst['cluster'] = lst_centr
    
    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)

    return(clst)


# In[3]:


clusters = km(model = model, clusters = int(args.clusters))


# In[5]:


# reading clusters
# import pandas as pd

# clusters = pd.read_csv("/home/stlk/Desktop/pwc/tsne_clust/output_cluster", names=["words", "cluster"], skiprows=1, 
                       # delimiter="\t")


# In[8]:


# importing bokeh library for interactive dataviz
import bokeh.plotting as bp
import bokeh.models as bmo
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, show, output_notebook
from bokeh.palettes import d3
from bokeh.models import ColumnDataSource, CategoricalColorMapper
# import seaborn as sns
from bokeh.palettes import brewer

def plot_tsne_interactive(model, words_number):
    
    # model = model
    # words_number = 300
    
    # getting a list of word vectors
    word_vectors = [model[w] for w in list(model.wv.vocab.keys())[:words_number]]

    # dimensionality reduction. No hope humans can seize dimensions higher than 5D
    from sklearn.manifold import TSNE
    tsne_model = TSNE(n_components = 2, verbose = 1, random_state = 0)
    tsne_model = tsne_model.fit_transform(word_vectors)

    tsne_df = pd.DataFrame(tsne_model, columns=['x', 'y'])
    tsne_df['words'] = list(model.wv.vocab.keys())[:words_number]
    tsne_df = pd.merge(tsne_df, clusters, how = "inner", on = "words")
    
    tsne_df['cluster'] = tsne_df['cluster'].astype(int)
    
    palette = ['#aec7e8', '#ff7f0e', '#ffbb78',  '#2ca02c',   '#98df8a',  '#d62728',  
    '#ff9896',  '#9467bd',  '#c5b0d5',  '#8c564b',  '#c49c94',  '#e377c2',  
    '#f7b6d2',    '#7f7f7f',  '#c7c7c7',  '#bcbd22',  '#dbdb8d',  '#17becf',
  '#9edae5']
    
    #  sns.palplot(sns.color_palette("hls", 8))
    
    # palette = d3['Category20'][len(tsne_df['cluster'].unique())]
    palette = palette[len(tsne_df['cluster'].unique())]
    # Create a map between factor and color.
    # colormap = {i: palette[i] for i in tsne_df['cluster'].unique()}
    colormap = dict(zip(tsne_df['cluster'].unique(), palette))
    #colormap1 = map(lambda x:)
    # Create a list of colors for each value that we will be looking at.
    
    # colors = [colormap[x] for x in tsne_df['cluster']]
    tsne_df['color'] = tsne_df['cluster']
    tsne_df.color.replace(colormap, inplace=True)
    # colormap = map(lambda palette: tsne_df['cluster'].unique, palette)
    # tsne_df['color'] = colors
    # tsne_df['cluster'] = tsne_df['cluster'].astype('category')
    
    # tsne_df.to_csv("/home/stlk/Desktop/pwc/tsne_clust/tsne_df.csv")
    #source = ColumnDataSource(dict(tsne_df)) # no need to make references to df
    
    # defining the chart
    #output_notebook()
    #plot_tfidf = bp.figure(plot_width=700, plot_height=600, title="A map of 10000 word vectors",
    #tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
    #x_axis_type=None, y_axis_type=None, min_border=1)

    # Interactivity of Bokeh
    #plot_tfidf.scatter(x='x',
     #              y='y', 
      #             color='color',
#                   legend='cluster',
#                   source=source)
#    hover = plot_tfidf.select(dict(type=HoverTool))
#    hover.tooltips={"word": "@words"}
#    
#    show(plot_tfidf)
    return(tsne_df)


# In[9]:


tsne_df = plot_tsne_interactive(model, int(args.words))
tsne_df.to_csv("/home/ruser/imdb/data/tsne_df.csv")

# tsne_df = pd.read_csv("/home/ruser/imdb/data/tsne_df.csv")



