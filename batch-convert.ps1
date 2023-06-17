# Input and output folder paths
$inputFolder = "E:/AudioClips/MyMusic/Gnuit"
$outputFolder = "E:/AudioClips/MyMusic/Gnuit/wav"

# Get a list of all .aiff files in the input folder
$aiffFiles = Get-ChildItem -Path $inputFolder -Filter *.aif

# Loop through each .aiff file and convert to .wav
foreach ($aiffFile in $aiffFiles) {
    # Output file path and name
    $wavFile = Join-Path -Path $outputFolder -ChildPath ($aiffFile.BaseName + ".wav")
    
    # Use ffmpeg to convert the file
    ffmpeg -i $aiffFile.FullName $wavFile
}

Write-Host "Batch conversion complete!"

