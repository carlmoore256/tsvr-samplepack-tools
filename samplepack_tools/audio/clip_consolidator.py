import os
import pandas as pd
from typing import List, Any
import numpy as np

import samplepack_tools.definitions as definitions
from samplepack_tools.audio.features import extract_features, windowed_mfccs
from samplepack_tools.utils import save_json, check_make_dir
from samplepack_tools.audio.audio_clip import AudioClip
from samplepack_tools.hashing import hash_list, hash_dict, hash_file
from samplepack_tools.publishing.resources import Resource, ResourceCategory


class ClipConsolidator:

    def __init__(self, clips: List[AudioClip] = []):
        self.clips = clips

    def add_clip(self, clip: AudioClip):
        self.clips.append(clip)

    def remove_clip(self, clip: AudioClip):
        self.clips.remove(clip)

    def render(
        self, clip_processors=None, master_processors=None, consolidate_processor=None
    ) -> AudioClip:
        max_channels = max([clip.channels for clip in self.clips])

        for clip in self.clips:
            clip.convert_to_channels(max_channels)
            if clip_processors is not None:
                for processor in clip_processors:
                    try:
                        clip.apply_processor(processor)
                    except Exception as e:
                        print(
                            f'ERROR: Processor {processor} failed on clip {clip.info["title"]} | {e}'
                        )

        samples = None
        if consolidate_processor is None:
            samples = np.concatenate(
                [clip.samples for clip in self.clips if clip.samples.shape[1] > 0],
                axis=1,
            )
        else:
            samples = consolidate_processor(
                [clip.samples for clip in self.clips if clip.samples.shape[1] > 0]
            )
        if samples is None:
            print(f"ERROR: Consolidate processor returned None")
            return None

        if master_processors is not None:
            for processor in master_processors:
                samples = processor(samples)
        return AudioClip.from_samples(samples)

    # def export_as_samplepack(self, title, samplepack_root=definitions.SAMPLEPACKS_ROOT, clip_processors=None, master_processors=None, consolidate_processor=None):
    #     clip = self.render(clip_processors, master_processors,
    #                        consolidate_processor)
    #     check_make_dir(samplepack_root)
    #     subfolder = os.path.join(samplepack_root, title)
    #     check_make_dir(subfolder)
    #     clip.save(os.path.join(subfolder, title + ".wav"), True)
    #     save_json(clip.info, os.path.join(subfolder, title + ".json"))

    # handles creating the sample package that can be distributed to TSVR
    # def publish(
    #     self,
    #     title: str,
    #     description: str = "",
    #     parameters=definitions.DEFAULT_PARAMETERS,
    #     creator=definitions.DEFAULT_CREATOR,
    #     additional_resources=[],
    #     session=definitions.EMPTY_SESSION,
    #     output_file=None,
    # ):
    #     # resources needs to be a list
    #     if isinstance(resources, Resource):
    #         resources = [resources]
    #     assert isinstance(resources, list)
    #     assert (
    #         filter(lambda x: x.category == ResourceCategory.AUDIO_SAMPLE, resources)
    #         is not None
    #     )
    #     audio_samples = list(
    #         filter(lambda x: x.category == ResourceCategory.AUDIO_SAMPLE, resources)
    #     )

    #     # the unique graincloud hash = hash(hash(sample), ..., hash(parameters))
    #     hash = hash_list([*[s.hash for s in audio_samples], hash_dict(parameters)])

    #     metadata = {
    #         "title": title if title is not None else auto_title(local_file),
    #         "description": description,
    #         "hash": hash,
    #         "creator": creator,
    #         "parameters": parameters,
    #         "resources": resources,
    #         "session": session,
    #     }
    #     if output_file is None:
    #         output_file = definitions.DATA_PATH + f"metadata/{metadata['hash']}.json"
    #     save_json(metadata, output_file)
    #     return metadata

    def export(
        self,
        outpath,
        clip_processors=None,
        master_processors=None,
        consolidate_processor=None,
    ):
        clip = self.render(clip_processors, master_processors, consolidate_processor)
        clip.save(outpath, True)

    def audio_features(self):
        all_features = []
        for clip in self.clips:
            try:
                features = extract_features(clip.samples[0])
                all_features.append(
                    {
                        "title": clip.info["title"],
                        "duration": clip.info["duration"],
                        **features,
                    }
                )
            except Exception as e:
                print(
                    f"failed to extract features for clip {
                      clip.info['title']} | {e}"
                )
        return pd.DataFrame(all_features)

    def plot_features_3d(
        self, x=("mfccs", 0), y=("mfccs", 1), z=("mfccs", 2), size="rms", color=None
    ):
        import plotly.express as px

        df_fig = self.audio_features()
        df_fig["x"] = df_fig[x[0]].apply(lambda d: d[x[1]])
        df_fig["y"] = df_fig[y[0]].apply(lambda d: d[y[1]])
        df_fig["z"] = df_fig[z[0]].apply(lambda d: d[z[1]])
        fig = px.scatter_3d(
            df_fig,
            x="x",
            y="y",
            z="z",
            size=size,
            color=color,
            opacity=0.8,
            hover_data=["title", "duration"],
        )
        return fig

    def compute_mfccs(self, window_size=16384, hop_size=16384, n_mfcc=10):
        all_features = []
        for clip in self.clips:
            features = windowed_mfccs(
                clip.samples[0],
                window_size=window_size,
                hop_size=hop_size,
                n_mfcc=n_mfcc,
            )
            for win_num, m in enumerate(features.T):
                mfccs = {f"mfcc_{i}": x for i, x in enumerate(m)}
                start_sample = win_num * hop_size
                end_sample = start_sample + window_size
                all_features.append(
                    {
                        "title": clip.info["title"],
                        "duration": clip.samples.shape[1],
                        "start_sample": start_sample,
                        "end_sample": end_sample,
                        "frac_idx": (start_sample + (window_size // 2))
                        / clip.samples.shape[1],
                        **mfccs,
                    }
                )
        return pd.DataFrame(all_features)
