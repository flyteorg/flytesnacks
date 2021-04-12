import pandera as pa

schema = pa.DataFrameSchema((
    {"col_*": pa.Column(pa.Check.Vae("file/path/to/weights"))}
)
schema.validate(df)

schema = pa.DataFrameSchema(
    {
        "column1": pa.Column(int),
        "column2": pa.Column(float),
    }
)
print(schema.example(size=3))
