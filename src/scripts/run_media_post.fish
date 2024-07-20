#!/usr/bin/env fish
# Using this above way of writing shebang can have some security concerns.
# See this stackoverflow thread: https://stackoverflow.com/a/72332845
# Since, I want this script to be portable for most of the users, instead of hardcoding like '#!/usr/bin/fish', I am using this way.

# Determine the script directory and virtual environment directory
set -l SCRIPT_DIR (dirname (realpath (status -f)))
set -l VENV_DIR "$SCRIPT_DIR/../../.venv"

# Check if two arguments are provided
if test (count $argv) -ne 2
    echo "ERROR: Usage: $0 {run_media_post_path} {temp_file_path}"
    exit 1
end

# Find the appropriate Python executable (python3 or python) in the system
set -l PYTHON_EXEC (command -v python3; or  command -v python)

# Ensure that the Python executable is available before creating the virtual environment
if not test -d "$VENV_DIR"
    if test -z "$PYTHON_EXEC"
        echo "ERROR: No suitable Python executable found."
        exit 1
    end
    "$PYTHON_EXEC" -m venv "$VENV_DIR"
end

if not test -x (command -v fish)
    echo "ERROR: Fish shell is not installed. Please install Fish."
    exit 1
end

# Activate the virtual environment if the shell is Fish
if test "$SHELL" = (command -v fish)
    # Check if the activate.fish file exists before sourcing it
    if test -f "$VENV_DIR/bin/activate.fish"
        source "$VENV_DIR/bin/activate.fish"
    else
        echo "ERROR: activate.fish not found in '$VENV_DIR/bin'"
        exit 1
    end
else
    echo "ERROR: Unsupported shell: '$SHELL'"
    exit 1
end

# Get the path to the python3 executable from the virtual environment
set -l PYTHON_EXEC (command -v python)

echo "this is the command that is going to run"
echo "$PYTHON_EXEC" "$argv[1]" "$argv[2]"
