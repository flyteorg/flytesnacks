NLP Processing
------------------------

In this tutorial, we will demonstrate how to process text data and generate word embeddings and visualisation
as part of Flyte workflow. The tutorial is based of the official Gensim `Word2Vec tutorial https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html`__
and `LDA guide https://radimrehurek.com/gensim/models/ldamodel.html`__.

About Gensim
===========

Gensim is a popular open source natural language processing (NLP) library used to process
large corpora (which can be larger than RAM) .
It has efficient multicore implementations of a number of algorithms such as  popular algorithms, such as
Latent Semantic Analysis (LSA/LSI/SVD), Latent Dirichlet Allocation (LDA) Word2Vec deep learning to perform
various complex tasks such as understanding document relationships, topic modelling, learning word
embeddings etc

You can read more about Gensim in the `Gensim Homepage https://radimrehurek.com/gensim/`__.

Data
====

The dataset used for this tutorial is the open source `Lee Background Corpus https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/test/test_data/lee_background.cor`__
included with the Gensim library installed with Python and does not need to be downloaded separately.


Steps of the Pipeline
======================

- Return a preprocessed (tokenised, stop words excluded, lemmatised) corpus from the
custom MyCorpus iterator
- Train Word2vec model using the preprocessed corpus
- Generate bag of words from corpus and train the LDA model
- Save the LDA and Word2Vec models to disk
- Deserialise the Word2Vec model and run word similarity and compute word movers distance
- Reduce the dimensionality (using tsne) and plot the word embeddings

Walkthrough
====================

Run workflows in this directory with the custom-built base image:

.. prompt:: bash $

     pyflyte run --remote word2vec_and_lda.py:nlp_workflow --image ghcr.io/flyteorg/flytecookbook:nlp_processing-latest


.. note::
  You will see multiple outputs on running the script, which would be associated with the serialised LDA and
  Word2Vec models. In addition, FlyteDeck is used to generate a plot rendered in html.
