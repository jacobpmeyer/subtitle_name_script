import os
import re

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
    """
    Format a new filename for anime episodes with season and episode numbers.

    Args:
        original_name (str): Original filename of the episode
        season (int): Season number
        episode (int): Episode number
        anime_name (str): Name of the anime, formatted for filenames
        is_subtitle (bool): Whether this is a subtitle file

    Returns:
        str: The formatted filename with season and episode numbers
    """
    # Format season and episode numbers with leading zeros
    s, e = str(season), str(episode)
    if len(s) < 2:
        s = f"0{season}"
    if len(e) < 2:
        e = f"0{episode}"

    # Get file extension
    file_ext = original_name.split('.')[-1]

    # Create the new filename based on whether anime_name was provided
    # Only add ".jpn" for subtitle files
    if anime_name:
        if is_subtitle:
            return f"{anime_name}_s{s}_e{e}.jpn.{file_ext}"
        else:
            return f"{anime_name}_s{s}_e{e}.{file_ext}"
    else:
        base_name = '.'.join(original_name.split('.')[:-1])  # Get filename without extension
        if is_subtitle:
            return f"{base_name}_s{s}_e{e}.jpn.{file_ext}"
        else:
            return f"{base_name}_s{s}_e{e}.{file_ext}"

def name_changer(directory, names, season, anime_name, is_subtitle, skip_confirmation=False):
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

    # Ask for confirmation if not skipping
    if not skip_confirmation:
        confirm = input("\nProceed with renaming? (y/n): ").lower().strip()
        if confirm != 'y':
            print("Operation cancelled.")
            return []
    else:
        print("Proceeding with renaming automatically...")

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

    # Check for season folders
    season_folders = detect_season_folders(selected_dir)
    total_renamed_files = 0

    if season_folders:
        print(f"\nFound {len(season_folders)} season folders. Processing all folders automatically.")

        # Sort season folders by season number
        season_folders.sort(key=lambda x: x[1])

        for folder_path, season_num in season_folders:
            folder_name = os.path.basename(folder_path)
            print(f"\nProcessing {folder_name} (Season {season_num})...")

            try:
                # List all files in the season directory
                files = os.listdir(folder_path)

                # Filter files based on the selected type
                target_files = [file for file in files if file.lower().endswith(target_extensions)]

                if not target_files:
                    print(f"No {file_type} files found in {folder_name}.")
                    continue

                print(f"Found {len(target_files)} {file_type} files.")

                # Process the files in this season folder
                renamed = name_changer(folder_path, target_files, season_num, anime_name, is_subtitle)

                if renamed:
                    total_renamed_files += len(renamed)
                    print(f"Renamed {len(renamed)} files in {folder_name}.")

            except OSError as e:
                print(f"Error accessing directory {folder_path}: {str(e)}")
                continue

    else:
        # No season folders found, process the main directory
        print("No season folders found. Processing main directory.")

        season_num = extract_season_number(os.path.basename(selected_dir))
        print(f"Using season {season_num} for main directory.")

        try:
            files = os.listdir(selected_dir)

            # Filter files based on the selected type
            target_files = [file for file in files if file.lower().endswith(target_extensions)]

            if not target_files:
                print(f"No {file_type} files found in the main directory.")
                return f"No {file_type} files found"

            print(f"Found {len(target_files)} {file_type} files.")

            # Process the files in the main directory
            renamed = name_changer(selected_dir, target_files, season_num, anime_name, is_subtitle)

            if renamed:
                total_renamed_files += len(renamed)

        except OSError as e:
            print(f"Error accessing directory {selected_dir}: {str(e)}")
            return "Failed"

    if total_renamed_files > 0:
        return f"Success! Renamed a total of {total_renamed_files} files across all folders."
    else:
        return "No files were renamed."

def auto_rename_files():
    """
    Automatically rename all subtitle and video files in all anime directories.
    Preserves anime names and season numbers.
    Only asks whether to rename subtitle or video files.
    """
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

    # Get all show directories
    try:
        show_dirs = [d for d in os.listdir(shows_dir) if os.path.isdir(os.path.join(shows_dir, d))]
    except Exception as e:
        print(f"Error accessing shows directory: {str(e)}")
        return "Failed"

    if not show_dirs:
        print("No show directories found.")
        return "Failed"

    # Display summary of what will be processed
    print(f"\nFound {len(show_dirs)} show directories to process.")
    print("This automated mode will:")
    print("- Process all show directories")
    print("- Extract anime names automatically from folder names")
    print("- Detect season folders and use appropriate season numbers")
    print("- Rename all files without individual confirmations")

    # Global confirmation
    confirm = input("\nDo you want to proceed with automatic processing of ALL shows? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Operation cancelled.")
        return "Operation cancelled by user."

    total_renamed_files = 0
    processed_shows = 0

    # Process each show directory
    for show_folder in show_dirs:
        show_path = os.path.join(shows_dir, show_folder)
        show_folder_name = os.path.basename(show_path)

        # Extract and format anime name
        inferred_anime_name = extract_anime_name(show_folder_name)
        anime_name = format_anime_name(inferred_anime_name)

        if not anime_name:
            print(f"Skipping {show_folder_name} - could not infer anime name")
            continue

        print(f"\nProcessing show: {show_folder_name}")
        print(f"Using anime name: {anime_name}")

        # Check for season folders
        season_folders = detect_season_folders(show_path)

        if season_folders:
            print(f"Found {len(season_folders)} season folders.")

            # Sort season folders by season number
            season_folders.sort(key=lambda x: x[1])

            for folder_path, season_num in season_folders:
                folder_name = os.path.basename(folder_path)
                print(f"Processing {folder_name} (Season {season_num})...")

                try:
                    # List all files in the season directory
                    files = os.listdir(folder_path)

                    # Filter files based on the selected type
                    target_files = [file for file in files if file.lower().endswith(target_extensions)]

                    if not target_files:
                        print(f"No {file_type} files found in {folder_name}.")
                        continue

                    print(f"Found {len(target_files)} {file_type} files.")

                    # Process the files in this season folder
                    renamed = name_changer(folder_path, target_files, season_num, anime_name, is_subtitle, skip_confirmation=True)

                    if renamed:
                        total_renamed_files += len(renamed)

                except OSError as e:
                    print(f"Error accessing directory {folder_path}: {str(e)}")
                    continue
        else:
            # No season folders found, process the main directory
            print("No season folders found. Processing main directory.")

            season_num = extract_season_number(show_folder_name)
            print(f"Using season {season_num} for main directory.")

            try:
                files = os.listdir(show_path)

                # Filter files based on the selected type
                target_files = [file for file in files if file.lower().endswith(target_extensions)]

                if not target_files:
                    print(f"No {file_type} files found in {show_folder_name}.")
                    continue

                print(f"Found {len(target_files)} {file_type} files.")

                # Process the files in the main directory
                renamed = name_changer(show_path, target_files, season_num, anime_name, is_subtitle, skip_confirmation=True)

                if renamed:
                    total_renamed_files += len(renamed)

            except OSError as e:
                print(f"Error accessing directory {show_path}: {str(e)}")
                continue

        processed_shows += 1

    if total_renamed_files > 0:
        return f"Success! Renamed a total of {total_renamed_files} files across {processed_shows} shows."
    else:
        return "No files were renamed."

if __name__ == "__main__":
    print("Anime Episode Filename Formatter")
    print("--------------------------------")
    print("1. Interactive Mode (select specific show and confirm changes)")
    print("2. Automatic Mode (process all shows with minimal confirmation)")

    while True:
        mode_choice = input("\nSelect mode (1/2): ").strip()
        if mode_choice in ['1', '2']:
            break
        print("Please enter 1 or 2.")

    if mode_choice == '1':
        result = get_names()
    else:
        result = auto_rename_files()

    print(result)
