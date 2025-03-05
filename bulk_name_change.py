import os

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

def name_changer(names, season, anime_name, is_subtitle):
    if not names:
        print("No files found in the current directory.")
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

        # Get the current directory where the script is running
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Create full paths for old and new names
        old_path = os.path.join(current_dir, name)
        new_path = os.path.join(current_dir, new_name)

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
    # Get the current directory where the script is running
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # List all files in the directory
    try:
        files = os.listdir(current_dir)
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
        print(f"No {file_type} files found in the current directory.")
        return f"No {file_type} files found"

    print(f"Found {len(target_files)} {file_type} files.")

    # Get season number from user
    while True:
        try:
            season_input = input("Enter season number: ")
            season = int(season_input)
            if season <= 0:
                print("Season number must be positive.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Get anime name from user
    anime_name = input("Enter anime name (leave blank to use original filenames): ").strip()

    # Format anime name: convert spaces to underscores, make lowercase, and
    # remove non-alpha characters
    if anime_name:
        anime_name = anime_name.replace(" ", "_")
        anime_name = anime_name.lower()
        anime_name = ''.join(char for char in anime_name if char.isalnum() or char == '_')
        print(f"Using formatted anime name: {anime_name}")

    renamed = name_changer(target_files, season, anime_name, is_subtitle)

    if renamed:
        return f"Success! Renamed {len(renamed)} files."

    return "No files were renamed."

if __name__ == "__main__":
    result = get_names()
    print(result)
