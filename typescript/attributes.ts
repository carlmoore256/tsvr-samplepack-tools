export enum AudioFeature {   
    Centroid,
    Spread,
    Flatness,
    Noiseness,
    Rolloff,
    Crest,
    Entropy,
    Decrease,
    Energy,
    RMS,
    ZCR,
    TimeEntropy,
    MFCC_0,
    MFCC_1,
    MFCC_2,
    MFCC_3,
    MFCC_4,
    MFCC_5,
    MFCC_6,
    MFCC_7,
    Contrast_0,
    Contrast_1,
    Contrast_2,
    Contrast_3,
    Contrast_4,
    Contrast_5,
    GrainIndex,
}

export interface Attributes {
    xFeature : AudioFeature; // chosen feature for x-axis
    yFeature : AudioFeature; // chosen feature for y-axis
    zFeature : AudioFeature; // chosen feature for z-axis
    rFeature : AudioFeature; // chosen feature for red axis
    gFeature : AudioFeature; // chosen feature for green axis
    bFeature : AudioFeature; // chosen feature for blue axis
    scaleFeature : AudioFeature; // chosen feature for scale (radius) axis
    windowSize : number; // size in samples of granular window
    hopSize : number; // size in samples of hops between windows
    scaleMult : number; // scale (radius) multiplier
    scaleExp : number; // scale (radius) exponential
    useHSV : boolean; // r_ax, g_ax, b_ax interpreted as h, s, v for coloring
    posAxisScale : [number]; // position is dot product of posAxisScale(x,y,z) & (x_ax, y_ax, z_ax)
}




function generateNFTAttributesArray(attributes : Attributes) : string {
    return JSON.stringify([
        {
            "trait_type": "x-feature",
            "value": AudioFeature[attributes.xFeature]
        },
        {
            "trait_type": "y-feature",
            "value": AudioFeature[attributes.yFeature]
        },
        {
            "trait_type": "z-feature",
            "value": AudioFeature[attributes.zFeature]
        },
        {
            "trait_type": "red-feature",
            "value": AudioFeature[attributes.rFeature]
        },
        {
            "trait_type": "green-feature",
            "value": AudioFeature[attributes.gFeature]
        },
        {
            "trait_type": "blue-feature",
            "value": AudioFeature[attributes.bFeature]
        },
        {
            "trait_type": "scale-feature",
            "value": AudioFeature[attributes.scaleFeature]
        },
        {
            "trait_type": "window-size",
            "value": attributes.windowSize
        },
        {
            "trait_type": "hop-size",
            "value": attributes.hopSize
        },
        {
            "trait_type": "scale-multiplier",
            "value": attributes.scaleMult
        },
        {
            "trait_type": "scale-exponential",
            "value": attributes.scaleExp
        },
        {
            "trait_type": "use-hsv",
            "value": attributes.useHSV
        },
        {
            "trait_type": "position-axis-scale",
            "value": attributes.posAxisScale
        }
    ]);
}

// export interface Attributes {
//     x_ax : AudioFeature; // chosen feature for x-axis
//     y_ax : AudioFeature; // chosen feature for y-axis
//     z_ax : AudioFeature; // chosen feature for z-axis
//     r_ax : AudioFeature; // chosen feature for red axis
//     g_ax : AudioFeature; // chosen feature for green axis
//     b_ax : AudioFeature; // chosen feature for blue axis
//     scl_ax : AudioFeature; // chosen feature for scale (radius) axis
//     win_size : number; // size in samples of granular window
//     hop_size : number; // size in samples of hops between windows
//     scl_mult : number; // scale (radius) multiplier
//     scl_exp : number; // scale (radius) exponential
//     use_hsv : boolean; // r_ax, g_ax, b_ax interpreted as h, s, v for coloring
//     pos_ax_scl : [number]; // apply dot product of this vector3 and x_ax, y_ax, z_ax
// }


// ERC-1155 Metadata Standard
// https://nftschool.dev/reference/metadata-schemas/#ethereum-and-evm-compatible-chains
// {
//     "title": "Token Metadata",
//     "type": "object",
//     "properties": {
//         "name": {
//             "type": "string",
//             "description": "Identifies the asset to which this token represents"
//         },
//         "decimals": {
//             "type": "integer",
//             "description": "The number of decimal places that the token amount should display - e.g. 18, means to divide the token amount by 1000000000000000000 to get its user representation."
//         },
//         "description": {
//             "type": "string",
//             "description": "Describes the asset to which this token represents"
//         },
//         "image": {
//             "type": "string",
//             "description": "A URI pointing to a resource with mime type image/* representing the asset to which this token represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
//         },
//         "properties": {
//             "type": "object",
//             "description": "Arbitrary properties. Values may be strings, numbers, object or arrays."
//         }
//     }
// }