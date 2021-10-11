import typing

from flytekit import workflow, task, dynamic, LaunchPlan, current_context


@task
def echo(s: str) -> str:
    return s


@workflow
def echo_wf(s: str) -> str:
    return echo(s=s)


echo_lp = LaunchPlan.get_default_launch_plan(current_context(), echo_wf)

STATIC_256_INPUT = "iE6WRzja4hOnuSyMy4hCOLdwwMWRe8IJ9ckLZqz8RhTyFpy6QtM4AYo9moyMyCgjijaio9WDT9bwwVSEe9mgIxtkMB0R8Pt71W7dZkFBMPp4OXgJkxl5qBDPDJozZsPumDJzY38wdxdqspg4wdUuX1pNKVvpIuER8UJy0YGKbtE4DjVuFnDhCefr2UiVZ1jKwpapCwPjRe4cHbSbqbDXIdpDSzffWipR3uvWcoltovy99CVexl6wL5ZWqin6S4ct "


@dynamic
def launch_lps(count: int) -> typing.List[str]:
    outputs = []
    for i in range(0, count):
        outputs.append(echo_lp(s=STATIC_256_INPUT))

    return outputs


@workflow
def wf(count: int) -> typing.List[str]:
    """
    Calls the dynamic workflow and returns the result"""

    # sending two strings to the workflow
    return launch_lps(count=count)


if __name__ == "__main__":
    print(wf(count=2))
