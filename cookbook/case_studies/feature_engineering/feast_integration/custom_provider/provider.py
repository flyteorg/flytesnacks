from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import pandas
from feast.entity import Entity
from feast.feature_table import FeatureTable
from feast.feature_view import FeatureView
from feast.infra.local import LocalProvider
from feast.infra.offline_stores.file_source import FileSource
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.registry import Registry
from feast.repo_config import RepoConfig
from flytekit.core.context_manager import FlyteContext
from tqdm import tqdm


class FlyteCustomProvider(LocalProvider):
    def __init__(self, config: RepoConfig, repo_path):
        super().__init__(config)

    def update_infra(
        self,
        project: str,
        tables_to_delete: Sequence[Union[FeatureTable, FeatureView]],
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_delete: Sequence[Entity],
        entities_to_keep: Sequence[Entity],
        partial: bool,
    ):
        # The update_infra method will be run during "feast apply" and is used to set up databases or launch
        # long-running jobs on a per table/view basis. This method should also clean up infrastructure that is unused
        # when feature views or tables are deleted. Examples of operations that update_infra typically fulfills
        # * Creating, updating, or removing database schemas for tables in an online store
        # * Launching a streaming ingestion job that writes features into an online store

        # Replace the code below in order to define your own custom infrastructure update operations
        super().update_infra(
            project,
            tables_to_delete,
            tables_to_keep,
            entities_to_delete,
            entities_to_keep,
            partial,
        )
        print("Launching custom streaming jobs is pretty easy...")

    def teardown_infra(
        self,
        project: str,
        tables: Sequence[Union[FeatureTable, FeatureView]],
        entities: Sequence[Entity],
    ):
        # teardown_infra should remove all deployed infrastructure

        # Replace the code below in order to define your own custom teardown operations
        super().teardown_infra(project, tables, entities)

    def online_write_batch(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        data: List[
            Tuple[EntityKeyProto, Dict[str, ValueProto], datetime, Optional[datetime]]
        ],
        progress: Optional[Callable[[int], Any]],
    ) -> None:
        # online_write_batch writes feature values to the online store
        super().online_write_batch(config, table, data, progress)

    def materialize_single_feature_view(
        self,
        config: RepoConfig,
        feature_view: FeatureView,
        start_date: datetime,
        end_date: datetime,
        registry: Registry,
        project: str,
        tqdm_builder: Callable[[int], tqdm],
    ) -> None:
        # materialize_single_feature_view loads the latest feature values for a specific feature value from the offline
        # store into the online store.
        # This method can be overridden to also launch custom batch ingestion jobs that loads the latest batch feature
        # values into the online store.

        # Replace the line below with your custom logic in order to launch your own batch ingestion job
        super().materialize_single_feature_view(
            config, feature_view, start_date, end_date, registry, project, tqdm_builder
        )
        print("Launching custom batch jobs is pretty easy...")

    def get_historical_features(
        self,
        config: RepoConfig,
        feature_views: List[FeatureView],
        feature_refs: List[str],
        entity_df: Union[pandas.DataFrame, str],
        registry: Registry,
        project: str,
        full_feature_names: bool,
    ) -> RetrievalJob:
        # get_historical_features returns a training dataframe from the offline store

        # We substitute the remote s3 file with a reference to a local file in each feature view being requested
        for fv in feature_views:
            if isinstance(fv.batch_source, FileSource):
                # Copy parquet file to a local file
                file_source: FileSource = fv.batch_source
                random_local_path = FlyteContext.current_context().file_access.get_random_local_path(file_source.path)
                FlyteContext.current_context().file_access.get_data(
                    file_source.path,
                    random_local_path,
                    is_multipart=True,
                )
                fv.batch_source=FileSource(
                    path=random_local_path,
                    event_timestamp_column=file_source.event_timestamp_column,
                )
        return super().get_historical_features(
            config,
            feature_views,
            feature_refs,
            entity_df,
            registry,
            project,
            full_feature_names,
        )

    def online_read(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        entity_keys: List[EntityKeyProto],
        requested_features: List[str] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, ValueProto]]]]:
        # get_historical_features returns a training dataframe from the offline store
        return super().online_read(config, table, entity_keys, requested_features)
