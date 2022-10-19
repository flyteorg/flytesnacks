@dsl.component(
    base_image='python:3.7',
    target_image='ghcr.io/my-project/my-component:v1',
    packages_to_install=['tensorflow'],
)
def train_model(
    dataset: Input[Dataset],
    model: Output[Model],
    num_epochs: int,
):
    ...


@task(
    container_image="{{.image.trainer.fqn }}:{{.image.trainer.version}}"
)
def train_model(
    dataset: pd.DataFrame,
    model: FlyteFile,
    num_epochs: int
):
    ...