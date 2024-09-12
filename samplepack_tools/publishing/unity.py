import datetime
import shutil
import glob
import json
import os

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

# make a json map of all files in resources
def make_resources_map(resources_path: str, ignore_files: list = ["resources-map.json", ".DS_Store"], ignore_ext: list = ["meta", "asset"]):
    resources_map = []
    for file in glob.glob(resources_path + "/**/*", recursive=True):
        if os.path.isdir(file):
            continue
        # if file in ignore_files:
        #     continue
        if file.split(".")[-1] in ignore_ext:
            continue
        # file_path = os.path.abspath(file).recplace("\\", "/")
        file_path = file.replace("\\", "/")
        file_name = file_path.replace(resources_path, "")
        if file_name.startswith("/"):
            file_name = file_name[1:]
        if file_name in ignore_files:
            continue
        resources_map.append({
            "file": file_name,
            "type": file_path.split(".")[-1],
            "bytes": os.stat(file_path).st_size,
            "created": datetime.datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
            "modified": datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
        })
    with open(os.path.join(resources_path, "resources-map.json"), "w") as f:
        json.dump(resources_map, f, indent=4)