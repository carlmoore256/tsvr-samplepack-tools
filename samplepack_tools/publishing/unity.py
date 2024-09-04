import os
import shutil
from samplepack_tools.utils import save_json
import samplepack_tools.definitions as definitions

def resources_subfolder(rel_path: str):
    path = os.path.join(definitions.UNITY_RESOURCES_PATH, rel_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def resources_samplepack_subfolder(title: str):
    path = os.path.join(definitions.UNITY_RESOURCES_PATH, definitions.UNITY_SAMPLE_PACKS_RESOURCE_FOLDER, title)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def format_resource_path(full_path: str):
    # remove anything in the path starting before "/Assets"
    path = full_path.split("/Resources")[-1]
    # remove any backslashes and format it correctly
    path = path.replace("\\", "/")
    if path[0] == "/":
        path = path[1:]
    # remove file extension
    path = path.split(".")[0]
    return path

def copy_file_to_unity_resources(local_file: str, rel_path: str):
    unity_resource_path = resources_subfolder(rel_path)
    unity_resource_path = os.path.join(unity_resource_path, os.path.basename(local_file))
    # os.system(f'cp "{local_file}" "{unity_resource_path}"')
    shutil.copyfile(local_file, unity_resource_path)
    return format_resource_path(unity_resource_path)

def save_json_to_unity_resources(data: dict, rel_path: str):
    unity_resource_path = resources_subfolder(rel_path)
    unity_resource_path = os.path.join(unity_resource_path, os.path.basename(rel_path))
    save_json(data, unity_resource_path)
    return format_resource_path(unity_resource_path)