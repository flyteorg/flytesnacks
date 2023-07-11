from dataclasses_json import dataclass_json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from flytekit.types.file import FlyteFile


@dataclass_json
@dataclass
class DelveAttribute:
    name: str
    value: FlyteFile
    upload: bool = False


@dataclass_json
@dataclass
class DelveArtifact:
    # This stores all the Delve Attributes
    name: str
    attributes: dict = field(default_factory=dict)
    archive: dict = field(default_factory=dict)
    history: list = field(default_factory=list)

    def add_attribute(self,
                      name: str,
                      value: FlyteFile,
                      upload: bool = False):

        attribute = DelveAttribute(name=name,
                                   value=value,
                                   upload=upload)
        if attribute.name in self.attributes:
            timestamp = datetime.now().strftime("-%Y-%m-%d-%H:%M:%S")
            self.archive[self.attributes[attribute.name].name + timestamp] = attribute
            self.attributes.pop(attribute.name)
        else:
            self.attributes[attribute.name] = attribute

    def __dir__(self):
        existing_attributes = super().__dir__()
        attributes = [name for name in self.attributes]

        return existing_attributes + attributes

    def __getattr__(self, name):
        attribute = self.attributes.get(name, None)
        if attribute:
            return attribute
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


@dataclass_json
@dataclass
class DelveArtifactContainer:
    # This lives with the DelveSeq Object
    artifacts: dict = field(default_factory=dict)
    archive: dict = field(default_factory=dict)

    def add_artifact(self, name: str):
        artifact = DelveArtifact(name=name)
        if artifact.name in self.artifacts and artifact == self.artifacts[name]:
            print(f'Archiving: {name}')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.archive[self.artifacts[name].name + '_' + timestamp] = self.artifacts[name]
            self.artifacts.pop(name)
        else:
            self.artifacts[name] = artifact

    def __getattr__(self, name):
        artifact = self.artifacts.get(name, None)
        if artifact:
            return artifact
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __dir__(self):
        existing_attributes = super().__dir__()
        attributes = [name for name in self.artifacts]

        return existing_attributes + attributes
