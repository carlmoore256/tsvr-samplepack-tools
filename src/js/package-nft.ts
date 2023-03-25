import { Attributes } from "./attributes";

export interface NFTMetadata {
    name: string;
    description: string;
    image: string;
    external_url: string;
    animation_url: string; // link to a video OR HTML page
    resources: {
        audio: string[]; // a list of audio files that will be loaded and concatenated in tsvr
        config: string; // a link to a JSON file containing any additional configuration
    };
    attributes: Attributes;
}


// function createMetadata()
