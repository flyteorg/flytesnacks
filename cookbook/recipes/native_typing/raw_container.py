from flytekit import ContainerTask, metadata, workflow, kwtypes


square = ContainerTask(
    name="square",
    metadata=metadata(),
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(val=int),
    outputs=kwtypes(out=int),
    image="alpine",
    command=["sh", "-c", "echo $(( {{.Inputs.val}} * {{.Inputs.val}} )) | tee /var/outputs/out"],
)

sum = ContainerTask(
    name="sum",
    metadata=metadata(),
    input_data_dir="/var/flyte/inputs",
    output_data_dir="/var/flyte/outputs",
    inputs=kwtypes(x=int, y=int),
    outputs=kwtypes(out=int),
    image="alpine",
    command=["sh", "-c", "echo $(( {{.Inputs.x}} + {{.Inputs.y}} )) | tee /var/flyte/outputs/out"],
)

@workflow
def raw_container_wf(val1: int, val2: int) -> int:
   return  sum(x=square(val=val1), y=square(val=val2))


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running raw_container_wf(val1=5, val2=5) {raw_container_wf(val1=5, val2=5)}")
