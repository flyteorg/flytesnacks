from typing import List, Tuple


def tower(n, source, destination, auxiliary) -> List[Tuple[int, int]]:
    if n == 1:
        return [(source, destination)]

    results = tower(n - 1, source, auxiliary, destination)
    results.append((source, destination))
    results.extend(tower(n - 1, auxiliary, destination, source))
    return results


def solve_tower(num_discs: int) -> int:
    results = tower(num_discs, 1, 3, 2)
    print(results)
    return len(results)


if __name__ == "__main__":
    print(solve_tower(num_discs=3))


@task
def model_parity_task(
    research_inference_execution_id: str,
    production_inference_execution_id: str,
    paritea_spec: str,  # noqa: BLK100
) -> str:
    """Placeholder tasks for the model score parity task. Takes workflows execution ids to go and get the correct outputs.
    Args:
        research_inference_execution_id (str): research run/model ID
        production_inference_execution_id (str): production run/model ID
    Returns:
        None: saves plot to output file
    """
    # Check if we want to skip

    paritea_data = PariteaSpec.from_spec(paritea_spec)
    if not paritea_data.model_parity:
        logging.info("Model Parity Skipped!")
        return json.dumps({"error_code": "skipped"})
    research_framework = paritea_data.research_framework_spec
    production_framework = paritea_data.production_framework_spec
    # Save the generated execution_id to the framework object
    research_framework.execution_id = research_inference_execution_id
    production_framework.execution_id = production_inference_execution_id
    # Create a context to load features from cloud storage to pull flyte inputs/ouputs
    with _common_utils.AutoDeletingTempDir("feature_dir") as feature_dir:
        with _data_proxy.LocalWorkingDirectoryContext(feature_dir):
            research_np_scores = research_framework.get_inference_scores()
            production_np_scores = production_framework.get_inference_scores()
            research_np_predictions = research_framework.get_inference_predictions()
            production_np_predictions = production_framework.get_inference_predictions()

