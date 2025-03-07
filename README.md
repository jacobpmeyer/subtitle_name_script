# Subtitle & Video Name Standardizer

A Python script that helps you batch rename subtitle and video files for TV shows and anime series, organizing them by season and episode numbers with a consistent naming convention.

## Overview

This script solves a common problem for media collectors: inconsistent file naming in TV shows and anime series. It automatically:

- Detects season information from folder names
- Extracts and formats show names
- Renames files in sequence with proper season and episode numbering
- Provides a preview of changes before applying them
- Works with both video files and subtitle files
- Offers both interactive and automatic processing modes

## Features

- Two operation modes:
  - **Interactive Mode**: Select specific shows and confirm changes
  - **Automatic Mode**: Process all shows with minimal confirmation
- Interactive folder selection from your media directory
- Automatic season detection and processing
- Smart show name extraction and formatting
- Preview of all file rename operations before execution
- Support for common video formats (.mp4, .mkv, .avi, .mov, .flv, .wmv)
- Support for subtitle formats (.srt, .ass, .vtt)
- Consistent naming convention:
  - Video files: `show_name_s01_e01.ext`
  - Subtitle files: `show_name_s01_e01.jpn.ext`
- Batch processing of all season folders within a show

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library modules)

## Installation

1. Clone this repository or download the `bulk_name_change.py` file
2. Ensure you have Python 3.6+ installed

## Usage

Run the script from the command line:

```
python bulk_name_change.py
```

First, select your preferred operation mode:
```
Anime Episode Filename Formatter
--------------------------------
1. Interactive Mode (select specific show and confirm changes)
2. Automatic Mode (process all shows with minimal confirmation)

Select mode (1/2):
```

### Interactive Mode

Follow the interactive prompts to:

1. Select your TV shows directory
2. Choose a specific show
3. Confirm or modify the extracted show name
4. Select if you're working with subtitle or video files
5. The script will automatically detect and process season folders if present
6. Review the preview of rename operations
7. Confirm to apply the changes

### Automatic Mode

The automatic mode processes all shows with minimal user interaction:

1. Select your TV shows directory
2. Specify if you're working with subtitle or video files
3. Confirm to process ALL shows in your directory
4. The script automatically:
   - Extracts show names from folder names
   - Detects season folders and numbers
   - Renames all files without individual confirmations

## Example Scenarios

### Example 1: Renaming anime subtitles

**Initial files:**
```
/Shows/Attack on Titan Season 1/
    sub01.ass
    sub02.ass
    sub03.ass
```

**After running the script:**
```
/Shows/Attack on Titan Season 1/
    attack_on_titan_s01_e01.jpn.ass
    attack_on_titan_s01_e02.jpn.ass
    attack_on_titan_s01_e03.jpn.ass
```

### Example 2: Renaming video files with season detection

**Initial files:**
```
/Shows/Breaking Bad/Season 2/
    Breaking.Bad.S02E01.720p.mkv
    Breaking.Bad.S02E02.720p.mkv
    Breaking.Bad.S02E03.720p.mkv
```

**After running the script:**
```
/Shows/Breaking Bad/Season 2/
    breaking_bad_s02_e01.mkv
    breaking_bad_s02_e02.mkv
    breaking_bad_s02_e03.mkv
```

### Example 3: Keeping original filenames but adding season/episode info

If you choose not to provide a show name when prompted, the script will keep the original filename and just add the season/episode information:

**Initial files:**
```
/Shows/Documentaries/Universe/
    The_Beginning.mp4
    Black_Holes.mp4
    Galaxies.mp4
```

**After running the script (without providing a show name):**
```
/Shows/Documentaries/Universe/
    The_Beginning_s01_e01.mp4
    Black_Holes_s01_e02.mp4
    Galaxies_s01_e03.mp4
```

### Example 4: Using Automatic Mode to process multiple shows

When using automatic mode, the script will process all shows in your directory:

```
Using TV shows directory: E:\Shows
Are you renaming subtitle or video files? (subtitle/video): subtitle

Found 5 show directories to process.
This automated mode will:
- Process all show directories
- Extract anime names automatically from folder names
- Detect season folders and use appropriate season numbers
- Rename all files without individual confirmations

Do you want to proceed with automatic processing of ALL shows? (y/n): y

Processing show: Attack on Titan Season 1
Using anime name: attack_on_titan
Found 1 subtitle files.
Proceeding with renaming automatically...
Renamed: sub01.ass → attack_on_titan_s01_e01.jpn.ass

Processing show: Breaking Bad
Using anime name: breaking_bad
Found 3 season folders.
Processing Season 1 (Season 1)...
Found 10 subtitle files.
Proceeding with renaming automatically...
[...]

Success! Renamed a total of 45 files across 5 shows.
```

## How It Works

1. The script first finds your media directory
2. Based on the selected mode (interactive or automatic):
   - **Interactive mode**: You select a specific show to process
   - **Automatic mode**: The script processes all shows
3. The script looks for season folders and processes them accordingly
4. It attempts to extract the show name from the folder name
5. Files are listed in alphabetical order and numbered sequentially
6. In interactive mode, the script shows a preview before applying changes
7. Subtitle files get a ".jpn" suffix added to their filenames

## Customization

The default TV shows directory is set to `E:\Shows`. If your media is stored elsewhere, you'll be prompted to provide the correct path.

## Troubleshooting

- **No files found**: Make sure you've selected the correct directory and file type
- **Error accessing directory**: Check file permissions
- **Incorrect season number**: The script extracts season numbers from folder names; if it's not correct, consider renaming your folders
- **Automatic mode skipping shows**: Ensure folder names contain recognizable show names

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you have suggestions for improvements.

## License

This script is provided as-is under the MIT License.
