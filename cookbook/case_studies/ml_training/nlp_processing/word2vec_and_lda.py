"""
.. _word2vec_and_lda:

Word Embeddings and Topic Modelling with Gensim
-----------------------------------------------

This example creates six Flyte tasks that:
1. Generate the sample dataset.
2. Train the word2vec model.
3. Train the LDA model and display the words per topic.
4. Compute word similarities.
5. Compute word movers distance.
6. Reduce dimensions using tsne and generate a plot using FlyteDeck.

"""

import logging

# %%
# First, we import the necessary libraries.
import os
import random
import typing
from dataclasses import dataclass
from typing import List, Tuple

import flytekit
import gensim
import matplotlib.pyplot as plt
import mpld3
import numpy as np
from dataclasses_json import dataclass_json
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

logger = logging.getLogger(__file__)

# %%
# We define the output file type.
MODELSER_NLP = typing.TypeVar("model")
model_file = typing.NamedTuple("ModelFile", model=FlyteFile[MODELSER_NLP])

# %%
# Next, we define the path to the Lee Corpus Dataset (installed with gensim).
data_dir = os.path.join(gensim.__path__[0], "test", "test_data")
lee_train_file = os.path.join(data_dir, "lee_background.cor")


# %%
# We will declare NamedTuples which will be used as signatures for the Flyte task outputs.
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
# We sample sentences of similar contexts to compare using the trained model.
SENTENCE_A = "Australian cricket captain has supported fast bowler"
SENTENCE_B = "Fast bowler received support from cricket captain"


# %%
# Data Generation
# ===============
#
# We define a function that carries out the following preprocessing steps on the dataset before training Word2Vec
# and LDA models:
# 1. Turns all words to lowercase and remove stopwords.
# 2. Splits the document into tokens using a regular expression tokenizer from NLTK.
# 3. Removes numeric single-character tokens as they do not tend to be useful, and the dataset contains a lot of them.
# 4. Uses the WordNet lemmatizer from NLTK and returns a list of lemmatized tokens.
def pre_processing(line: str) -> List[str]:
    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(remove_stopwords(line.lower()))
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


# %%
# Next, we implement an iterator that calls the ``pre_processing`` function on each input sentence from the corpus
# and yields the processed results.
class MyCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __init__(self, path):
        self.corpus_path = datapath(path)

    def __iter__(self):
        for line in open(self.corpus_path):
            yield pre_processing(line)


# %%
# We define a Flyte task to generate the processed corpus containing a list of tokenized sentence lists.
@task
def generate_processed_corpus() -> List[List[str]]:
    # Set file names for train and test data
    sentences_train = MyCorpus(lee_train_file)
    train_corpus = list(sentences_train)
    return train_corpus


# %%
# Hyperparameters
# ===============
#
# Next we create a dataclass for Word2Vec model hyperparameters comprising the following parameters:
#
# - ``min_count``:  Prunes the dictionary and removes low-frequency words.
# - ``vector_size``: Number of dimensions (N) of the N-dimensional space that gensim Word2Vec maps the words onto.
#   Bigger size values require more training data but can lead to better (more accurate) models.
# - ``workers``: For training parallelization to speed up training.
# - ``compute_loss``: To toggle computation of loss while training the Word2Vec model.
@dataclass_json
@dataclass
class Word2VecModelHyperparams(object):
    """
    Hyperparameters that can be used while training the word2vec model.
    """

    min_count: int = 1
    vector_size: int = 200
    workers: int = 4
    compute_loss: bool = True


# %%
# Similarly we create a dataclass for LDA model hyperparameters:
#
# - ``num_topics``: The number of topics to be extracted from the training corpus.
# - ``alpha``: A-priori belief on document-topic distribution. In `auto` mode, the model learns this from the data.
# - ``passes``: Controls how often the model is trained on the entire corpus or number of epochs.
# - ``chunksize``:  Controls how many documents are processed at a time in the training algorithm. Increasing the
#   chunk size speeds up training, at least as long as the chunk of documents easily fits into memory.
# - ``update_every``: Number of documents to be iterated through for each update.
# - ``random_state``: Seed for reproducibility.
@dataclass_json
@dataclass
class LDAModelHyperparams(object):
    """
    Hyperparameters that can be used while training the LDA model.
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
# Next we initialize and train the Word2Vec model on the preprocessed corpus using hyperparameters defined
# in the dataclass.
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
    logger.info(f"training loss: {training_loss}")
    out_path = os.path.join(
        flytekit.current_context().working_directory, "word2vec.model"
    )
    model.save(out_path)
    return (out_path,)


# %%
# We transform the documents to a vectorized form and compute the frequency of each word to generate a bag of
# word corpus for the LDA model to train on. We also create a mapping from word IDs to words as input to
# the LDA model for training.
@task
def train_lda_model(
    corpus: List[List[str]], hyperparams: LDAModelHyperparams
) -> model_file:
    id2word = Dictionary(corpus)
    bow_corpus = [id2word.doc2bow(doc) for doc in corpus]
    id_words = [[(id2word[id], count) for id, count in line] for line in bow_corpus]
    logger.info(f"sample of bag of words generated: {id_words[:2]}")
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
    logger.info(f"Shows words in each topic: {lda.print_topics(num_words=5)}")
    file = "lda.model"
    lda.save(file)
    return (file,)


# %%
# Word Similarities
# =================
#
# We deserialize the model from disk and compute the top 10 similar
# words to the given word in the corpus (we will use the word `computer` when running
# the workflow to output similar words). Note that since the model is trained
# on a small corpus, some of the relations might not be clear.
@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def word_similarities(model_ser: FlyteFile[MODELSER_NLP], word: str):
    model = Word2Vec.load(model_ser.path)
    wv = model.wv
    logger.info(f"Word vector for {word}:{wv[word]}")
    logger.info(
        f"Most similar words in corpus to {word}: {wv.most_similar(word, topn=10)}"
    )


# %%
# Sentence Similarity
# ===================
#
# We define a task that computes the Word Mover’s Distance (WMD) metric using the trained embeddings of words.
# This enables us to assess the distance between two documents in a meaningful way even when they have
# no words in common.
# WMD outputs a large value for two completely unrelated sentences and small value for two closely related
# sentences.
# Since we chose two similar sentences for comparison, the word movers distance
# should be small. You can try altering either ``SENTENCE_A`` or ``SENTENCE_B`` variables to be dissimilar
# to the other sentence, and check if the value computed is larger.
@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def word_movers_distance(model_ser: FlyteFile[MODELSER_NLP]) -> float:
    sentences = [SENTENCE_A, SENTENCE_B]
    results = []
    for i in sentences:
        result = [w for w in utils.tokenize(i) if w not in STOPWORDS]
        results.append(result)
    model = Word2Vec.load(model_ser.path)
    distance = model.wv.wmdistance(*results)
    logger.info(f"Computing word movers distance for: {SENTENCE_A} and {SENTENCE_B} ")
    logger.info(f"Word Movers Distance is {distance}")
    return distance


# %%
# Dimensionality Reduction and Plotting
# =====================================
#
# The word embeddings made by the model can be visualized after reducing the dimensionality to two with tSNE.
@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def dimensionality_reduction(model_ser: FlyteFile[MODELSER_NLP]) -> plotdata:
    model = Word2Vec.load(model_ser.path)
    num_dimensions = 2
    vectors = np.asarray(model.wv.vectors)
    labels = np.asarray(model.wv.index_to_key)
    tsne = TSNE(n_components=num_dimensions, random_state=0)
    vectors = tsne.fit_transform(vectors)
    x_vals = [v[0] for v in vectors]
    y_vals = [v[1] for v in vectors]
    return x_vals, y_vals, labels


# %%
# We can now visualise the word embeddings with a matplotlib plot.
@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def plot_with_matplotlib(x, y, labels):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x, y)
    indices = list(range(len(labels)))
    selected_indices = random.sample(indices, 25)
    for i in selected_indices:
        plt.annotate(labels[i], (x[i], y[i]))
    flytekit.Deck("Word Embeddings", mpld3.fig_to_html(fig))


# %%
# Running the Workflow
# ====================
#
# Lastly we define a workflow to call the aforementioned tasks.
# This will return the Word2Vec and LDA models as workflow outputs.
@workflow
def nlp_workflow() -> workflow_outputs:
    corpus = generate_processed_corpus()
    model_wv = train_word2vec_model(
        training_data=corpus, hyperparams=Word2VecModelHyperparams()
    )
    model_lda = train_lda_model(corpus=corpus, hyperparams=LDAModelHyperparams())
    word_similarities(model_ser=model_wv.model, word="computer")
    word_movers_distance(model_ser=model_wv.model)
    axis_labels = dimensionality_reduction(model_ser=model_wv.model)
    plot_with_matplotlib(
        axis_labels["x_values"], axis_labels["y_values"], axis_labels["labels"]
    )
    return model_wv.model, model_lda.model


# %%
# Finally, we can run the workflow locally.
if __name__ == "__main__":
    logger.info(f"Running {__file__} main...")
    print(nlp_workflow())
