"""
.. _word2vec_and_lda:

Word Embeddings and Topic Modelling using Gensim
------------------------------------------------

This script will create six Flyte tasks, that will:

1. Generate the sample dataset
2. Train the word2vec model.
3. Train the LDA model and display the words per topic
4. Compute word similarities
5. Compute word movers distance
6. Reduce dimensions using tsne and generate a plot using FlyteDeck

Let's get started with the example!

"""

# %%
# First, we need to import some libraries.
import os
import random
import typing
from dataclasses import dataclass
from pprint import pprint
from pprint import pprint as print
from typing import List, Tuple
import mpld3
import gensim
import matplotlib.pyplot as plt
import numpy as np
from dataclasses_json import dataclass_json
import flytekit
from flytekit import Resources, task, workflow
from flytekit.types.file import FlyteFile
from gensim import utils
from gensim.corpora import Dictionary
from gensim.models import LdaModel, Word2Vec
from gensim.parsing.preprocessing import STOPWORDS, remove_stopwords
from gensim.test.utils import datapath
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sklearn.manifold import TSNE

# %%
# Here we define the output file type. This is useful in
# combining tasks, where one task may only accept models serialized in ``.model``
MODELSER_NLP = typing.TypeVar("model")
model_file = typing.NamedTuple("ModelFile", model=FlyteFile[MODELSER_NLP])

# %%
# Define the path to the Lee Corpus Dataset (installed with gensim)
data_dir = os.path.join(gensim.__path__[0], "test", "test_data")
lee_train_file = os.path.join(data_dir, "lee_background.cor")


# %%
# Declare NamedTuples which will be used as signatures for the Flyte task outputs.
# The variable names and types correspond to the values of the unpacked tuples returned
# from the corresponding Flyte task.
plotdata = typing.NamedTuple(
    "PlottingData",
    x_values=typing.List[np.float32],
    y_values=typing.List[np.float32],
    labels=np.array,
)

bowdata = typing.NamedTuple(
    "BagOfWordsOutput",
    bow=List[List[Tuple]],
    id2word=List[List[Tuple]],
)

workflow_outputs = typing.NamedTuple(
    "WorkflowOutputs",
    word2vecmodel=FlyteFile[MODELSER_NLP],
    ldamodel=FlyteFile[MODELSER_NLP],
)


# %%
# Sample sentences of very similar context to compare using the trained model
SENTENCE_A = "Australian cricket captain has supported fast bowler"
SENTENCE_B = "Fast bowler received support from cricket captain"


# %%
# Data Generation
# ========
#
# This function carries out the preprocessing steps on the dataset before training both models.
# First we turn all words to lower case and remove stopwords. We then split the document
# into tokens using a regular expression tokenizer from NLTK. We remove numeric tokens and tokens
# that are only a single character, as they don’t tend to be useful, and the dataset contains a
# lot of them. We then use the WordNet lemmatizer from NLTK and return a list of lemmatised tokens.
def pre_processing(line: str) -> List[str]:
    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(remove_stopwords(line.lower()))
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


# %%
# Here we implement an iterator that yields one sentence after another. It calls the
#  ``pre_processing`` function on each input sentence from the corpus and yields the processed
#  results.
class MyCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __init__(self, path):
        self.corpus_path = datapath(path)

    def __iter__(self):
        for line in open(self.corpus_path):
            yield pre_processing(line)


# %%
# We define the first Flyte task to generate the processed corpus containing a list of
# tokenised sentence lists.
@task
def generate_processed_corpus() -> List[List[str]]:
    # Set file names for train and test data
    sentences_train = MyCorpus(lee_train_file)
    train_corpus = list(sentences_train)
    return train_corpus


# %%
# Hyperparameters
# ========
#
# It is also possible in Flyte to pass custom objects, as long as they are
# declared as ``dataclass``es and also decorated with ``@dataclass_json``.
# Here we create a dataclass for Word2Vec model hyperparameters.
# 1. min_count:  for pruning the dictionary and removing low frequency words
# 2. vector_size: number of dimensions (N) of the N-dimensional space that gensim
# Word2Vec maps the words onto.Bigger size values require more training data, but can
# lead to better (more accurate) models.
# 3. workers: For training parallelization, to speed up training
# 4. compute_loss:  can be used to toggle computation of loss while training the Word2Vec model.
@dataclass_json
@dataclass
class Word2VecModelHyperparams(object):
    """
    These are the word-to-vec hyper parameters which can be set for training.
    """

    min_count: int = 1
    vector_size: int = 200
    workers: int = 4
    compute_loss: bool = True


# %%
# Similarly we create a dataclass for LDA model hyperparameters:
# 1. num_topics: The number of topics to be extracted from the training corpus.
# 2. alpha: A-priori belief on document-topic distribution. Set this to `auto` so the model learns this
# from the data.
# 3. passes: Controls how often we train the model on the entire corpus or number of epochs.
# 4. chunksize:  Controls how many documents are processed at a time in the training
# algorithm. Increasing chunksize will speed up training, at least as long as the chunk of documents
# easily fit into memory.
# 5. update_every : Number of documents to be iterated through for each update.
# 6. random_state: seed for reproducibility
@dataclass_json
@dataclass
class LDAModelHyperparams(object):
    """
    These are the lda model hyper parameters which can be set for training.
    """

    num_topics: int = 5
    alpha: str = "auto"
    passes: int = 10
    chunksize: int = 100
    update_every: int = 1
    random_state: int = 100

# %%
# Training
# ========
#
# This task initialises and trains the Word2Vec model on the preprocessed corpus using
# the hyperparameters defined in the dataclass. It prints the training loss to the user and
# serialises the model to disk.
@task
def train_word2vec_model(
    training_data: List[List[str]], hyperparams: Word2VecModelHyperparams
) -> model_file:

    model = Word2Vec(
        training_data,
        min_count=hyperparams.min_count,
        workers=hyperparams.workers,
        vector_size=hyperparams.vector_size,
        compute_loss=hyperparams.compute_loss,
    )
    training_loss = model.get_latest_training_loss()
    print(f"training loss: {training_loss}")
    file = "word2vec.model"
    model.save(file)
    return (file,)


# %%
# Here we train the LDA model using the hyperparameters from the dataclass.
# Before this we need to transform the documents to a vectorized form and compute the frequency of each word
# to generate a bag of word corpus for the LDA model to train on. We also need to create a mapping
# from word IDs to words as input to the LDA model for training. The words in each topic are printed
# out once the model has finished training. Finally, the model is serialised to disk.
@task
def train_lda_model(
    corpus: List[List[str]], hyperparams: LDAModelHyperparams
) -> model_file:
    id2word = Dictionary(corpus)
    bow_corpus = [id2word.doc2bow(doc) for doc in corpus]
    id_words = [[(id2word[id], count) for id, count in line] for line in bow_corpus]
    print(f"sample of bag of words generated: {id_words[:2]}")
    lda = LdaModel(
        corpus=bow_corpus,
        id2word=id2word,
        num_topics=hyperparams.num_topics,
        alpha=hyperparams.alpha,
        passes=hyperparams.passes,
        chunksize=hyperparams.chunksize,
        update_every=hyperparams.update_every,
        random_state=hyperparams.random_state,
    )
    pprint(f"Shows words in each topic: {lda.print_topics(num_words=5)}")
    file = "lda.model"
    lda.save(file)
    return (file,)


# %%
# Word Similarities
# ========
#
# The model is deserialised from disk and used to compute the top 10 most similar
# words in a corpus to a given word (we will use the word `computer` when running
# the workflow to output the similar words). Note that since the model is trained
# on a small corpus, some of the relations might not be so clear.
@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def word_similarities(model_ser: FlyteFile[MODELSER_NLP], word: str):
    model = Word2Vec.load(model_ser.path)
    wv = model.wv
    print(f"Word vector for {word}:{wv[word]}")
    print(f"Most similar words in corpus to {word}: {wv.most_similar(word, topn=10)}")


# %%
# Sentence Similarity
# ========
#
# This helper function creates a word embeddings matplotlib plot
# rendered using FlyteDeck and output as html.
@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def word_movers_distance(model_ser: FlyteFile[MODELSER_NLP]) -> float:
    sentences = [SENTENCE_A, SENTENCE_B]
    results = []
    for i in sentences:
        result = [w for w in utils.tokenize(i) if w not in STOPWORDS]
        results.append(result)
    model = Word2Vec.load(model_ser.path)
    distance = model.wv.wmdistance(*results)
    print(f"Computing word movers distance for: {SENTENCE_A} and {SENTENCE_B} ")
    print(f"Word Movers Distance is {distance} (lower means closer)")
    return distance


# %%
# Dimensionality Reduction and Plotting
# ========
#
# This helper function creates a word embeddings matplotlib plot
# rendered using FlyteDeck and output as html.
def plot_with_matplotlib(x, y, labels):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(x, y)
    indices = list(range(len(labels)))
    selected_indices = random.sample(indices, 25)
    for i in selected_indices:
        plt.annotate(labels[i], (x[i], y[i]))
    flytekit.Deck("Word Embeddings", mpld3.fig_to_html(fig))


# %%
# The word embeddings made by the model can be visualised by reducing
# dimensionality of the words to 2 dimensions using tSNE.
# This task calls the ``plot_with_matplotlib`` function to generate the word
# embeddings plot after dimensionality reduction.
@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def tsne_and_plot(model_ser: FlyteFile[MODELSER_NLP]) -> plotdata:
    model = Word2Vec.load(model_ser.path)
    num_dimensions = 2
    vectors = np.asarray(model.wv.vectors)
    labels = np.asarray(model.wv.index_to_key)
    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)
    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    plot_with_matplotlib(x_vals, y_vals, labels)
    return x_vals, y_vals, labels


# %%
# Running the Workflow
# ========
#
# Next, we define a workflow to call the aforementioned tasks.
# This will return both models as workflow outputs
@workflow
def nlp_workflow() -> workflow_outputs:
    corpus = generate_processed_corpus()
    model_wv = train_word2vec_model(
        training_data=corpus, hyperparams=Word2VecModelHyperparams()
    )
    model_lda = train_lda_model(corpus=corpus, hyperparams=LDAModelHyperparams())
    word_similarities(model_ser=model_wv.model, word="computer")
    word_movers_distance(model_ser=model_wv.model)
    tsne_and_plot(model_ser=model_wv.model)
    return (model_wv.model, model_lda.model)


# %%
# Finally, we can run the workflow locally.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(nlp_workflow())
