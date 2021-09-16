import os
from typing import Type
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from feast import repo_config
from feast.feature_store import FeatureStore
from feast.repo_config import RepoConfig
from flytekit import FlyteContext
from flytekit.core.type_engine import TypeEngine, TypeTransformer
from flytekit.models.literals import Literal, Scalar
from flytekit.models.types import LiteralType, SimpleType
from feast.infra.offline_stores.file import FileOfflineStoreConfig
from feast.infra.online_stores.sqlite import SqliteOnlineStoreConfig
from feast import FeatureStore as FeastFeatureStore
from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToDict
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from feast.entity import Entity
from feast.feature_view import FeatureView
from feast.feature_service import FeatureService


@dataclass_json
@dataclass
class FeatureStoreConfig:
    registry_path: str
    project: str
    online_store_remote_path: str


@dataclass_json
@dataclass
class FeatureStore:
    config: FeatureStoreConfig

    def _initialize_s3_env_vars(self):
        # TODO: guard these assignments behind a check
        os.environ["FEAST_S3_ENDPOINT_URL"] = os.environ["FLYTE_AWS_ENDPOINT"]
        os.environ["AWS_ACCESS_KEY_ID"] = os.environ["FLYTE_AWS_ACCESS_KEY_ID"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ["FLYTE_AWS_SECRET_ACCESS_KEY"]

    def apply(
        self,
        objects: Union[
            Entity,
            FeatureView,
            FeatureService,
            List[Union[FeatureView, Entity, FeatureService]],
        ],
    ):
        self._initialize_s3_env_vars()

        config = RepoConfig(
            registry=self.config.registry_path,
            project=self.config.project,
            # Notice the use of a custom provider.
            provider="custom_provider.provider.FlyteCustomProvider",
            offline_store=FileOfflineStoreConfig(),
            # TODO: comment this assumption
            online_store=SqliteOnlineStoreConfig(path='online.db'),
        )
        fs = FeastFeatureStore(config=config)
        fs.apply(objects)

        # Applying also initializes the sqlite tables in the online store
        FlyteContext.current_context().file_access.upload('online.db', "s3://feast-integration/online.db")


class FeatureStoreTransformer(TypeTransformer[FeatureStore]):
    def __init__(self):
        super().__init__(name="FeatureStore", t=FeatureStore)

    def get_literal_type(self, t: Type[FeatureStore]) -> LiteralType:
        return LiteralType(simple=SimpleType.STRUCT, metadata={})

    def to_literal(
        self,
        ctx: FlyteContext,
        python_val: FeatureStore,
        python_type: Type[FeatureStore],
        expected: LiteralType,
    ) -> Literal:

        if not isinstance(python_val, FeatureStore):
            raise AssertionError(f'Value cannot be converted to a feature store: {python_val}')

        s = Struct()
        s.update(python_val.to_dict())
        return Literal(Scalar(generic=s))

    def to_python_value(
        self,
        ctx: FlyteContext,
        lv: Literal,
        expected_python_type: Type[FeatureStore],
    ) -> FeatureStore:
        if not (lv and lv.scalar and lv.scalar.generic and "config" in lv.scalar.generic):
            raise ValueError("FeatureStore requires a valid FeatureStoreConfig to load python value")

        conf_dict = MessageToDict(lv.scalar.generic["config"])
        feature_store_config = FeatureStoreConfig(**conf_dict)
        return FeatureStore(config=feature_store_config)

        # # TODO: guard these assignments behind a check
        # os.environ["FEAST_S3_ENDPOINT_URL"] = os.environ["FLYTE_AWS_ENDPOINT"]
        # os.environ["AWS_ACCESS_KEY_ID"] = os.environ["FLYTE_AWS_ACCESS_KEY_ID"]
        # os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ["FLYTE_AWS_SECRET_ACCESS_KEY"]

        # config = RepoConfig(
        #     registry=feature_store_config.registry_path,
        #     project=feature_store_config.project,
        #     # Notice the use of a custom provider.
        #     provider="custom_provider.provider.FlyteCustomProvider",
        #     offline_store=FileOfflineStoreConfig(),
        #     # TODO: comment this assumption
        #     online_store=SqliteOnlineStoreConfig(path='online.db'),
        # )

        # return Fea

TypeEngine.register(FeatureStoreTransformer())
