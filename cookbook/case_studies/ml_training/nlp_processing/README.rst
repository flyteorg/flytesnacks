NLP Processing
------------------------

In this tutorial, we will demonstrate how to process text data and train word2vec and
lda models and generate plots as part of Flyte workflow.
The tutorial is based of the official `gensim` tutorials on [word2vec](https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html)
and [lda](https://radimrehurek.com/gensim/models/ldamodel.html).
The dataset used for this tutorial is the open source [Lee Background Corpus](https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/test/test_data/lee_background.cor)
included with the `Gensim` library.


Steps of the Pipeline
======================

1. Return a preprocessed (tokenised, stop words excluded, lemmatised) corpus from the
custom MyCorpus iterator
2. Train Word2vec model using the preprocessed corpus
4. Generate bag of words from corpus and train the LDA model
4. Save the LDA and Word2Vec models to disk
5. Deserialise the Word2Vec model and run word similarity and compute word movers distance
6. Reduce the dimensionality (using tsne) and plot the word embeddings

Walkthrough
====================

Run workflows in this directory with the custom-built base image:

.. prompt:: bash $

     pyflyte run --remote word2vec_and_lda.py:nlp_workflow --image ghcr.io/flyteorg/flytecookbook:nlp_processing-latest
