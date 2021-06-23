###
SQL
###

Flyte tasks are not always restricted to running user-supplied containers, nor even containers at all. Indeed, this is
one of the most important design decisions in Flyte. Non-container tasks can have arbitrary targets for execution -
example an API that executes SQL queries like SnowFlake, BigQuery, a synchronous WebAPI etc.
