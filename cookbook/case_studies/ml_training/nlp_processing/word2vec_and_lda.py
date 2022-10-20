"""
.. _word2vec_and_lda:

Word Embeddings and Topic Modelling using Gensim
------------------------------------------------

`Gensim <https://radimrehurek.com/gensim/>`__ is an fast library for processing large corpus of unstructred data
using data streamed algorithms. It also published pre-trained models for a number of domains and allows custom training
of word embeddings.

In this tutorial, we will demostrate a workflow to preprocess the `Lee Background Corpus
https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/test/test_data/lee_background.cor` and create word
embeddings and topic models using Gensim, and Flyte.

We will split the generated dataset into train, test and validation set.

Next, we will create six Flyte tasks, that will:

1. Generate the sample dataset
2. Train the word2vec model.
3. Train the LDA model and display the words per topic
4. Compute word similarities
5. Compute word movers distance
6. Reduce dimensions using tsne and generate a plot using FlyteDeck


Let's get started with the example!

"""


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


# typing for serialised model file
MODELSER_NLP = typing.TypeVar("model")
model_file = typing.NamedTuple("ModelFile", model=FlyteFile[MODELSER_NLP])

# Set file names for train and test data
test_data_dir = os.path.join(gensim.__path__[0], "test", "test_data")
lee_train_file = os.path.join(test_data_dir, "lee_background.cor")

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


SENTENCE_A = "Australian cricket captain has supported fast bowler"
SENTENCE_B = "Fast bowler received support from cricket captain"


class MyCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __init__(self, path):
        self.corpus_path = datapath(path)

    def __iter__(self):
        for line in open(self.corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield pre_processing(line)


def pre_processing(line: str) -> List[str]:
    tokenizer = RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(remove_stopwords(line.lower()))
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


@task
def generate_processed_corpus() -> List[List[str]]:
    # Set file names for train and test data
    sentences_train = MyCorpus(lee_train_file)
    train_corpus = list(sentences_train)
    return train_corpus


# %%
# It is also possible in Flyte to pass custom objects, as long as they are
# declared as ``dataclass``es and also decorated with ``@dataclass_json``.
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


@task
def train_word2vec_model(
    training_data: List[List[str]], hyperparams: Word2VecModelHyperparams
) -> model_file:
    # instantiating and training the Word2Vec model
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


@task(cache_version="1.0", cache=True, limits=Resources(mem="200Mi"))
def word_similarities(model_ser: FlyteFile[MODELSER_NLP], word: str):
    model = Word2Vec.load(model_ser.path)
    wv = model.wv
    print(f"Word vector for {word}:{wv[word]}")
    print(f"Most similar words in corpus to {word}: {wv.most_similar(word, topn=10)}")


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


def plot_with_matplotlib(x, y, labels):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(x, y)
    indices = list(range(len(labels)))
    selected_indices = random.sample(indices, 25)
    for i in selected_indices:
        plt.annotate(labels[i], (x[i], y[i]))
    flytekit.Deck("Word Embeddings", mpld3.fig_to_html(fig))


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


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(nlp_workflow())
