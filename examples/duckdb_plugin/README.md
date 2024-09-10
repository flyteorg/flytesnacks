(duckdb)=

# DuckDB

```{eval-rst}
.. tags:: Integration, Data, Analytics, Beginner
```

[DuckDB](https://duckdb.org/) is an in-process SQL OLAP database management system that is explicitly designed to achieve high performance in analytics. MotherDuck is a collaborative data warehouse that extends the power of DuckDB to the cloud.

The Flytekit DuckDB plugin facilitates the efficient execution of intricate analytical queries within your workflow either in-process with DuckDB, on the cloud with MotherDuck, or a hybrid of the two.

To install the Flytekit DuckDB plugin, run the following command:

```
pip install flytekitplugins-duckdb
```

The Flytekit DuckDB plugin includes the {py:class}`~flytekitplugins:flytekitplugins.duckdb.DuckDBQuery` task, which allows you to specify the following parameters:

- `query`: The DuckDB query to execute. This is optional as it can be passed at initialization or run time.
- `inputs`: The query parameters to be used during query execution. This can be a StructuredDataset, a string or a list.
- `provider`: This is a {py:class}`~flytekitplugins:flytekitplugins.duckdb.DuckDBProvider` or a callable that facilitates the connection to a remote database if desired.

```{auto-examples-toc}
duckdb_example
```
