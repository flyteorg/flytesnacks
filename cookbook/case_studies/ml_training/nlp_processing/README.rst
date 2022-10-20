NLP Processing
------------------------

In this tutorial, we will demonstrate how to process text data and generate word embeddings and visualisation
as part of Flyte workflow. The tutorial follows the steps in the official Gensim `Word2Vec tutorial <https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html>`__
and `LDA guide <https://radimrehurek.com/gensim/models/ldamodel.html>`__ with some modifications.

About Gensim
===========

Gensim is a popular open source natural language processing (NLP) library used to process
large corpora (which can be larger than RAM) .It has efficient multicore implementations of a number
of algorithms such as  popular algorithms, such as `Latent Semantic Analysis <http://lsa.colorado.edu/papers/dp1.LSAintro.pdf>`__, `Latent Dirichlet Allocation (LDA) <https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf>`__,
`Word2Vec deep learning <https://arxiv.org/pdf/1301.3781.pdf>`__ to perform various complex tasks such as understanding document relationships, topic modelling, learning word
embeddings etc.

You can read more about Gensim in the `Gensim Homepage <https://radimrehurek.com/gensim/>`__.

Data
====

The dataset used for this tutorial is the open source `Lee Background Corpus <https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/test/test_data/lee_background.cor>`__
included with the Gensim library installed with Python and does not need to be downloaded separately.


Steps of the Pipeline
======================

- Return a preprocessed (tokenised, stop words excluded, lemmatised) corpus from the custom iterator.
- Train Word2vec model using the preprocessed corpus.
- Generate bag of words from corpus and train the LDA model.
- Save the LDA and Word2Vec models to disk.
- Deserialise the Word2Vec model and run word similarity and compute word movers distance.
- Reduce the dimensionality (using tsne) and plot the word embeddings.

.. note::
  You will see multiple outputs once the pipeline completes. These would be associated with the serialised LDA and
  Word2Vec models. In addition, FlyteDeck is used to generate a plot rendered in html. By default, all these files should be
  stored in the directory in which the script is being run from.

Walkthrough
====================

Run workflows in this directory with the custom-built base image:

.. prompt:: bash $

     pyflyte run --remote word2vec_and_lda.py:nlp_workflow --image ghcr.io/flyteorg/flytecookbook:nlp_processing-latest

