from flytekit import dynamic, kwtypes, task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema
from flytekitplugins.athena import AthenaConfig, AthenaTask

# %%
# This is the world's simplest query. Note that in order for registration to work properly, you'll need to give your
# Athena task a name that's unique across your project/domain for your Flyte installation.
athena_task_no_io = AthenaTask(
    name="sql.athena.no_io",
    inputs={},
    query_template="""
        select 1
    """,
    output_schema_type=None,
    task_config=AthenaConfig(database="mnist"),
)


@workflow
def no_io_wf():
    return athena_task_no_io()


# %%
# Of course, in real world applications we are usually more interested in using Athena to query a dataset.
# In this case we assume that the vaccinations table exists and has been populated data according to this schema
#     +----------------------------------------------+
#     | country (string)                             |
#     +----------------------------------------------+
#     | iso_code (string)                            |
#     +----------------------------------------------+
#     | date (string)                                |
#     +----------------------------------------------+
#     | total_vaccinations (string)                  |
#     +----------------------------------------------+
#     | people_vaccinated (string)                   |
#     +----------------------------------------------+
#     | people_fully_vaccinated (string)             |
#     +----------------------------------------------+
#     | daily_vaccinations_raw (string)              |
#     +----------------------------------------------+
#     | daily_vaccinations (string)                  |
#     +----------------------------------------------+
#     | total_vaccinations_per_hundred (string)      |
#     +----------------------------------------------+
#     | people_vaccinated_per_hundred (string)       |
#     +----------------------------------------------+
#     | people_fully_vaccinated_per_hundred (string) |
#     +----------------------------------------------+
#     | daily_vaccinations_per_million (string)      |
#     +----------------------------------------------+
#     | vaccines (string)                            |
#     +----------------------------------------------+
#     | source_name (string)                         |
#     +----------------------------------------------+
#     | source_website (string)                      |
#     +----------------------------------------------+
#
# Let's look out how we can parameterize our query to filter results for a specific country.
# We'll produce a FlyteSchema that we can use in downstream flyte tasks for further analysis or manipulation.

athena_task_templatized_query = AthenaTask(
    name="sql.athena.w_io",
    inputs=kwtypes(limit=int),
    task_config=AthenaConfig(database="vaccinations"),
    query_template="""
    SELECT * FROM vaccinations where iso_code like  {{ .inputs.iso_code }}
    """,
    output_schema_type=FlyteSchema,
)

# %%
# Now we (trivially) clean up and interact with the data produced from the above Athena query in a separate Flyte task.
@task
def manipulate_athena_schema(s: FlyteSchema) -> FlyteSchema:
    df = s.open().all()
    return df[df.total_vaccinations.notnull()]


@workflow
def full_hive_demo_wf(country_iso_code: str) -> FlyteSchema:
    demo_schema = athena_task_templatized_query(iso_code=country_iso_code)
    return manipulate_athena_schema(s=demo_schema)
