#!/usr/bin/env bash
# Using this above way of writing shebang can have some security concerns.
# See this stackoverflow thread: https://stackoverflow.com/a/72332845
# Since, I want this script to be portable for most of the users, instead of hardcoding like '#!/usr/bin/bash', I am using this way.

# Determine the script directory and virtual environment directory
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SCRIPT_DIR/../../.venv"

# Check if both arguments are provided
if [ $# -ne 2 ]; then
  echo "ERROR: Usage: $0 {run_media_post_path} {temp_file_path}"
  exit 1
fi

# Find the appropriate Python executable
PYTHON_EXEC=$(command -v python3 || command -v python)

# Ensure that the Python executable is available before creating the virtual environment
if [ ! -d "$VENV_DIR" ]; then
  if [ -z "$PYTHON_EXEC" ]; then
    echo "ERROR: No suitable Python executable found."
    exit 1
  fi
  "$PYTHON_EXEC" -m venv "$VENV_DIR"
fi

# Activate the virtual environment based on the shell type
if [[ "$SHELL" == *"/bash" || "$SHELL" == *"/sh" ]]; then
    # Check if the activate file exists before sourcing it
    if [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
    else
        echo "ERROR: activate file not found in '$VENV_DIR/bin' directory"
        exit 1
    fi
else
    echo "ERROR: Unsupported shell: $SHELL"
    exit 1
fi

# Set the python executable to the one from the virtual environment
PYTHON_EXEC=$(command -v python)

"$PYTHON_EXEC" "$1" "$2"
