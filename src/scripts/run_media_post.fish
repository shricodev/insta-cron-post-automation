#!/usr/bin/env fish
# Using this above way of writing shebang can have some security concerns.
# See this stackoverflow thread: https://stackoverflow.com/a/72332845
# Since, I want this script to be portable for most of the users, instead of hardcoding like '#!/usr/bin/fish', I am using this way.

# Constants for error messages
set -l ERROR_USAGE "ERROR: Usage: $0 {media_post_path} {post_file_path}"
set -l ERROR_FILE_NOT_FOUND "ERROR: One or both of the files do not exist or are not valid files."
set -l ERROR_PYTHON_NOT_FOUND "ERROR: No suitable Python executable found."
set -l ERROR_FISH_NOT_INSTALLED "ERROR: Fish shell is not installed. Please install Fish."
set -l ERROR_ACTIVATE_NOT_FOUND "ERROR: activate.fish not found in '$VENV_DIR/bin'"
set -l ERROR_UNSUPPORTED_SHELL "ERROR: Unsupported shell: '$SHELL'"

# Determine the script and virtual environment directory
set -l SCRIPT_DIR (dirname (realpath (status -f)))
set -l VENV_DIR (realpath "$SCRIPT_DIR/../../.venv")

function print_usage_and_exit
    echo $ERROR_USAGE
    exit 1
end

# Check if two arguments are provided
if test (count $argv) -ne 2
    print_usage_and_exit
end

# Function to check if a file exists and has the correct extension
function check_file
    set -l file_path "$argv[1]"
    set -l expected_extension "$argv[2]"

    if not test -f "$file_path"
        echo $ERROR_FILE_NOT_FOUND
        exit 1
    end

    if not string match -q "*.$expected_extension" "$file_path"
        echo "ERROR: The file '$file_path' must be a .$expected_extension file."
        exit 1
    end
end

# Validate the provided files
check_file "$argv[1]" "py"
check_file "$argv[2]" "json"

# Extract and validate arguments
set -l MEDIA_POST_PATH (realpath "$argv[1]")
set -l POST_FILE_PATH (realpath "$argv[2]")

# Find the appropriate Python executable (python3 or python) in the system
set -l PYTHON_EXEC (command -v python3; or  command -v python)

# Ensure that the Python executable is available before creating the virtual environment
if not test -d "$VENV_DIR"
    if test -z "$PYTHON_EXEC"
        echo $ERROR_PYTHON_NOT_FOUND
        exit 1
    end
    "$PYTHON_EXEC" -m venv "$VENV_DIR"
end

if not test -x (command -v fish)
    echo $ERROR_FISH_NOT_INSTALLED
    exit 1
end

# Activate the virtual environment if the shell is Fish
if test "$SHELL" = (command -v fish)
    # Check if the activate.fish file exists before sourcing it
    if test -f "$VENV_DIR/bin/activate.fish"
        source "$VENV_DIR/bin/activate.fish"
    else
        echo $ERROR_ACTIVATE_NOT_FOUND
        exit 1
    end
else
    echo $ERROR_UNSUPPORTED_SHELL
    exit 1
end

# Get the path to the python3 executable from the virtual environment
set -l PYTHON_EXEC (command -v python)

"$PYTHON_EXEC" "$MEDIA_POST_PATH" "$POST_FILE_PATH"

# Remove the cronjob after running the script
crontab -l | grep -v "$POST_FILE_PATH" | crontab -
