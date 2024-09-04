from samplepack_tools.utils import (
    get_mimetype,
    get_file_size,
    auto_title,
    save_temp_data,
    datestamp,
)
from samplepack_tools.hashing import hash_file
import samplepack_tools.definitions as definitions
from samplepack_tools.publishing.unity import (
    copy_file_to_unity_resources,
    format_resource_path,
)

from samplepack_tools.utils import save_json, load_json
import json
from enum import Enum


class ResourceCategory(Enum):
    AUDIO_SAMPLE = "AudioSample"
    THUMBNAIL = "Thumbnail"
    SAMPLEPACK = "SamplePack"
    SETTINGS = "Settings"

    def __str__(self):
        return self.value
    

class Resource:
    def __init__(self, local_file: str, category: ResourceCategory, title: str = None):
        self.local_file = local_file
        type = get_mimetype(local_file)
        assert type in definitions.RESOURCE_TYPES
        # make sure the category is valid
        assert category in ResourceCategory.__members__.values()

        self.hash = hash_file(local_file)
        self.num_bytes = get_file_size(local_file)
        self.title = title if title is not None else auto_title(local_file)

        self.category = category
        self.type = type

        self.appdata_uri = None
        self.unity_uri = None
        self.web_uri = None

    def copy_to_unity_resources(self):
        if self.local_file is None:
            raise ValueError("No local file to copy to Unity resources")
        resource_dir = f"{
            definitions.UNITY_SAMPLE_PACKS_RESOURCE_FOLDER}/{self.title}"
        self.unity_uri = copy_file_to_unity_resources(self.local_file, resource_dir)
        print(f"Copied {self.local_file} to Unity resources: {self.unity_uri}")
        save_temp_data(self.to_dict(), "resources", f"{self.hash}_{datestamp()}.json")

    def publish_to_web(self, web_provider: callable):
        if self.local_file is None:
            raise ValueError("No local file to publish to web")
        self.web_uri = web_provider(self.local_file)
        print(f"Published {self.local_file} to web: {self.web_uri}")
        save_temp_data(self.to_dict(), "resources", f"{self.hash}_{datestamp()}.json")

    def to_dict(self):
        return {
            "type": self.type,
            "category": str(self.category),
            "title": self.title,
            "hash": self.hash,
            "bytes": self.num_bytes,
            "unityUri": self.unity_uri,
            "webUri": self.web_uri,
            "appdataUri": self.appdata_uri,
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    def from_json(self, json_file):
        raw_data = load_json(json_file)
        self.type = raw_data["type"]
        self.category = ResourceCategory[raw_data["category"]]
        self.title = raw_data["title"]
        self.hash = raw_data["hash"]
        self.num_bytes = raw_data["bytes"]
        self.unity_uri = raw_data["unityUri"]
        self.web_uri = raw_data["webUri"]
        self.appdata_uri = raw_data["appdataUri"]
    
    def __dict__(self):
        return self.to_dict()
    
    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)