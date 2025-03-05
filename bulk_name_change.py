import os
import sys
import re
from difflib import get_close_matches

def select_folder(base_path):
    """
    Allow user to select a folder from the base path using a numbered list.
    """
    try:
        # Get all subdirectories in the base path
        subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

        if not subdirs:
            print(f"No subdirectories found in {base_path}")
            return None

        # List all folders with numbers for selection
        print(f"\nAvailable folders in {base_path}:")
        for idx, folder in enumerate(subdirs, 1):
            print(f"{idx}. {folder}")

        # Let user select a folder by number
        while True:
            selection = input("\nSelect a folder number: ")
            if selection.isdigit() and 1 <= int(selection) <= len(subdirs):
                selected_folder = subdirs[int(selection)-1]
                return os.path.join(base_path, selected_folder)
            else:
                print("Invalid selection. Try again.")
    except Exception as e:
        print(f"Error while accessing {base_path}: {str(e)}")
        return None

def detect_season_folders(directory):
    """
    Detect season folders in the given directory.
    Returns a list of tuples (folder_path, season_number)
    """
    try:
        # Get all subdirectories
        subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

        # Look for season folders
        season_folders = []
        season_pattern = re.compile(r'season\s*(\d+)', re.IGNORECASE)

        for folder in subdirs:
            match = season_pattern.search(folder)
            if match:
                season_number = int(match.group(1))
                season_folders.append((os.path.join(directory, folder), season_number))

        return season_folders
    except Exception as e:
        print(f"Error detecting season folders: {str(e)}")
        return []

def extract_season_number(folder_name):
    """
    Extract season number from folder name.
    Returns season number if found, otherwise returns 1.
    """
    season_pattern = re.compile(r'season\s*(\d+)', re.IGNORECASE)
    match = season_pattern.search(folder_name)

    if match:
        return int(match.group(1))
    return 1  # Default to season 1 if no season number found

def extract_anime_name(folder_name):
    """
    Extract anime name from folder name.
    Removes season information and cleans up the name.
    """
    # Remove season information
    season_pattern = re.compile(r'\s*season\s*\d+\s*', re.IGNORECASE)
    cleaned_name = season_pattern.sub(' ', folder_name).strip()

    # Remove common separators and clean up
    separators = ['_', '.', '-', '–', '—']
    for sep in separators:
        cleaned_name = cleaned_name.replace(sep, ' ')

    # Remove excess whitespace and format
    cleaned_name = ' '.join(cleaned_name.split())

    return cleaned_name

def format_anime_name(anime_name):
    """
    Format anime name for filename:
    - Replace spaces with underscores
    - Make lowercase
    - Remove non-alphanumeric characters
    """
    if not anime_name:
        return ""

    formatted_name = anime_name.replace(" ", "_")
    formatted_name = formatted_name.lower()
    formatted_name = ''.join(char for char in formatted_name if char.isalnum() or char == '_')

    return formatted_name

def format_new_filename(original_name, season, episode, anime_name, is_subtitle):
    # Format season and episode numbers with leading zeros
    s, e = str(season), str(episode)
    if len(s) < 2:
        s = f"0{season}"
    if len(e) < 2:
        e = f"0{episode}"

    # Get file extension
    file_ext = original_name.split('.')[-1]

    # Create the new filename based on whether anime_name was provided
    # Only add ".ja" for subtitle files
    if anime_name:
        return f"{anime_name}_s{s}_e{e}.{file_ext}"
    else:
        base_name = '.'.join(original_name.split('.')[:-1])  # Get filename without extension
        return f"{base_name}_s{s}_e{e}.{file_ext}"

def name_changer(directory, names, season, anime_name, is_subtitle):
    if not names:
        print("No files found in the selected directory.")
        return []

    names.sort()
    episode = 1
    renamed_files = []

    # Show preview of changes
    print("\nPreview of file renames:")
    for name in names:
        new_name = format_new_filename(name, season, episode, anime_name, is_subtitle)
        print(f"{name} → {new_name}")
        episode += 1

    # Ask for confirmation
    confirm = input("\nProceed with renaming? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Operation cancelled.")
        return []

    # Reset episode counter for actual renaming
    episode = 1

    for name in names:
        new_name = format_new_filename(name, season, episode, anime_name, is_subtitle)

        # Create full paths for old and new names
        old_path = os.path.join(directory, name)
        new_path = os.path.join(directory, new_name)

        try:
            # Rename the file
            os.rename(old_path, new_path)
            renamed_files.append(new_name)
            print(f"Renamed: {name} → {new_name}")
        except OSError as e:
            print(f"Error renaming {name}: {str(e)}")

        # Increment episode counter for next file
        episode += 1

    return renamed_files

def get_names():
    # Define the TV shows directory
    shows_dir = "E:\\Shows"

    # Check if the directory exists
    if not os.path.isdir(shows_dir):
        print(f"Error: TV shows directory not found at {shows_dir}")
        shows_dir = input("Please enter the path to your TV shows directory: ")
        if not os.path.isdir(shows_dir):
            print(f"Error: Directory not found at {shows_dir}")
            return "Failed"

    print(f"Using TV shows directory: {shows_dir}")

    # Let user select a show folder using simple numbered selection
    selected_dir = select_folder(shows_dir)
    if not selected_dir:
        return "Failed to select a show directory"

    show_folder_name = os.path.basename(selected_dir)
    print(f"Selected show directory: {show_folder_name}")

    # Extract anime name from the show folder
    inferred_anime_name = extract_anime_name(show_folder_name)
    print(f"Inferred anime name: {inferred_anime_name}")

    # Check for season folders
    season_folders = detect_season_folders(selected_dir)

    working_dir = selected_dir
    season_num = 1  # Default season number
    in_season_folder = False

    if season_folders:
        print("\nFound season folders:")
        for idx, (folder_path, season_number) in enumerate(season_folders, 1):
            folder_name = os.path.basename(folder_path)
            print(f"{idx}. {folder_name} (Season {season_number})")

        # Let user select a season folder or use the current folder
        while True:
            selection = input("\nSelect a season folder number or press Enter to use the show directory: ")
            if not selection:
                # Use the show directory, extract season number if possible
                season_num = extract_season_number(os.path.basename(selected_dir))
                print(f"Using show directory with season {season_num}")
                break
            elif selection.isdigit() and 1 <= int(selection) <= len(season_folders):
                idx = int(selection) - 1
                working_dir, season_num = season_folders[idx]
                in_season_folder = True
                print(f"Selected season folder: {os.path.basename(working_dir)} (Season {season_num})")
                break
            else:
                print("Invalid selection. Try again.")
    else:
        # No season folders found, extract season number from the directory name if possible
        season_num = extract_season_number(os.path.basename(selected_dir))
        print(f"No season folders found. Using season {season_num}")

    # Change to the working directory
    try:
        os.chdir(working_dir)
    except OSError as e:
        print(f"Error changing to directory {working_dir}: {str(e)}")
        return "Failed"

    # List all files in the directory
    try:
        files = os.listdir(working_dir)
    except OSError as e:
        print(f"Error accessing directory: {str(e)}")
        return "Failed"

    # Ask user if they're working with subtitle or video files
    while True:
        file_type = input("Are you renaming subtitle or video files? (subtitle/video): ").lower().strip()
        if file_type in ['subtitle', 'video']:
            break
        print("Please enter either 'subtitle' or 'video'.")

    is_subtitle = file_type == 'subtitle'

    # Define file extensions based on type
    if is_subtitle:
        target_extensions = ('.srt', '.ass', '.vtt')
        print("Looking for subtitle files (.srt, .ass, .vtt)...")
    else:
        target_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv')
        print(f"Looking for video files {target_extensions}...")

    # Filter files based on the selected type
    target_files = [file for file in files if file.lower().endswith(target_extensions)]

    if not target_files:
        print(f"No {file_type} files found in the selected directory.")
        return f"No {file_type} files found"

    print(f"Found {len(target_files)} {file_type} files.")
    print(f"Using season number: {season_num}")

    # Format the inferred anime name
    formatted_inferred_name = format_anime_name(inferred_anime_name)

    # Ask user if the inferred anime name is correct
    if formatted_inferred_name:
        print(f"Inferred anime name: {inferred_anime_name}")
        print(f"Formatted for filenames: {formatted_inferred_name}")

        confirm = input("Use this anime name? (y/n): ").lower().strip()
        if confirm == 'y':
            anime_name = formatted_inferred_name
        else:
            # If user rejects, prompt for a new name
            anime_name = input("Enter anime name (leave blank to use original filenames): ").strip()
            if anime_name:
                anime_name = format_anime_name(anime_name)
    else:
        # If no name could be inferred, prompt for a name
        anime_name = input("Enter anime name (leave blank to use original filenames): ").strip()
        if anime_name:
            anime_name = format_anime_name(anime_name)

    if anime_name:
        print(f"Using formatted anime name: {anime_name}")

    renamed = name_changer(working_dir, target_files, season_num, anime_name, is_subtitle)

    if renamed:
        return f"Success! Renamed {len(renamed)} files."

    return "No files were renamed."

if __name__ == "__main__":
    result = get_names()
    print(result)
