import typing

from flytekit.core.class_based_resolver import ClassStorageTaskResolver


class Builder(ClassStorageTaskResolver):

    def __init__(self, query):
        self._query = query
        self._process = None
        super().__init__()

    @classmethod
    def read(cls, query):
        return cls(query=query)

    def process(self, fn: typing.Callable):
        self._process = fn


    def name(self) -> str:
        return "ClassStorageTaskResolver"

    def get_all_tasks(self) -> List[PythonAutoContainerTask]:
        return list(self.mapping.keys())

    def add(self, user_function: Callable):
        fn = PythonFunctionTask(task_config=None, task_function=user_function, task_resolver=cls)
        self.mapping[fn] = user_function

    def load_task(self, loader_args: List[str]) -> PythonAutoContainerTask:
        if len(loader_args) != 1:
            raise RuntimeError(f"Unable to load task, received ambiguous loader args {loader_args}, expected only one")

        # string should be parseable a an int
        print(loader_args[0])
        idx = int(loader_args[0])
        k = list(self.mapping.keys())

        return self.mapping[k[idx]]

    def loader_args(self, settings: SerializationSettings, t: PythonAutoContainerTask) -> List[str]:
        """
        This is responsible for turning an instance of a task into args that the load_task function can reconstitute.
        """
        if t not in self.mapping:
            raise Exception("no such task")

        return [f"{list(cls.mapping.keys()).index(t)}"]


    def build(self):
        @task

        @workflow
        def wf_fn():


my_wf = Builder.read("select *")
    .process(transform)
    .build()

my_wf(project="my-gcp-project", runner="DirectRunner")
