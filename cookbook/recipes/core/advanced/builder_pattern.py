from flytekit import task, workflow


@task
def tsk_write(in1: str):
    print(f"Write task {in1}")


class Builder:
    def __init__(self, query: str):
        self.do_fn = None
        self.query = query

    @staticmethod
    def create(query: str = None):
        return Builder(query)

    def assign_function(self, do_fn):
        self.do_fn = do_fn
        return self

    def build(self):
        @task
        def my_task() -> str:
            print(f"In nested task, query is {self.query}")
            self.do_fn()
            return "hello from the inner function"

        @workflow
        def my_wf() -> None:
            inner_task_output = my_task()
            tsk_write(in1=inner_task_output)

        return my_wf, my_task


def transform():
    print("In transform")


sample_query = "select * from my_input_table"
my_wf, my_task = Builder.create(sample_query).assign_function(transform).build()


if __name__ == "__main__":
    my_wf()
    print(f"WF {my_wf}, Task {my_task}")
