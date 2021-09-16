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
        for feature_view in feature_views:
            if not isinstance(feature_view.batch_source, FileSource):
                continue
            # Copy parquet file to a local file
            file_source: FileSource = feature_view.batch_source
            random_local_path = FlyteContext.current_context().file_access.get_random_local_path(file_source.path)
            FlyteContext.current_context().file_access.get_data(
                file_source.path,
                random_local_path,
                is_multipart=True,
            )
            feature_view.batch_source=FileSource(
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

    def _localize_feature_view(self, feature_view: FeatureView):
        """
        This function ensures that the `FeatureView` object points to files in the local disk
        """
