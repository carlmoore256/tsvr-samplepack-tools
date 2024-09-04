from samplepack_tools.publishing.resources import Resource
from samplepack_tools.publishing.web_storage import aws_web_provider
import samplepack_tools.definitions as definitions
from samplepack_tools.hashing import hash_dict, hash_list
from samplepack_tools.publishing.resources import ResourceCategory
import json
from typing import List
import os


class GrainCloud:

    def __init__(self, resources: List[Resource] = []): # type: ignore
        if not isinstance(resources, list):
            resources = [resources]
        self.resources: List[Resource] = resources
        self.parameters = definitions.DEFAULT_PARAMETERS

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

    @property   
    def audio_resources(self):
        # return all resources that are audio samples
        return list(
            filter(
                lambda x: x.category == ResourceCategory.AUDIO_SAMPLE, self.resources
            )
        )

    def hash(self):
        # get the hash of each audio resource
        print()
        audio_hashes = [r.hash for r in self.audio_resources]
        # combine the audio hashes with the parameters hash
        return hash_list(audio_hashes + [hash_dict(self.parameters)])

    def publish(
        self,
        title: str,
        description: str = "",
        creator: dict = definitions.DEFAULT_CREATOR,
        session: dict = definitions.EMPTY_SESSION,
        web_provider=aws_web_provider,
    ):
        if not os.path.exists("data/grain_clouds"):
            os.makedirs("data/grain_clouds")
        output_file = f"data/grain_clouds/{self.hash()}.json"

        # find any audio resource
        if len(self.resources) == 0:
            raise ValueError("No audio resource provided")
        
        if len(self.audio_resources) == 0:
            raise ValueError("GrainCloud must have at least 1 audio resource to publish")

        for resource in self.resources:
            if resource.web_uri is None:
                print(f"Publishing resource to web: {resource.title}")
                try:
                    resource.publish_to_web(web_provider)
                except Exception as e:
                    print(f'Error publishing resource {resource.title}: {e}')

        metadata = {
            "title": title,
            "description": description,
            "hash": self.hash(),
            "creator": creator,
            "parameters": self.parameters,
            "resources": [r.to_dict() for r in self.resources],
            "session": session,
        }

        with open(output_file, "w") as f:
            f.write(json.dumps(metadata, indent=4))

        print("Uploading metadata")
        try:
            url = web_provider(output_file)
            print(f"Uploaded metadata to {url}")
        except Exception as e:
            print(e)
        return metadata
