"""Compile code into Ableton Remote Script directory"""
import os
import py_compile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def compileTo(destination_dir, source_dir):
    # Retrieve the PATH environment variable
    if not destination_dir:
        print("Error: environment variable not set.")
        exit(1)

    # Print the destination directory for confirmation
    print(f"Destination Directory: {destination_dir}")

    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        print(f"Creating destination directory: {destination_dir}")
        os.makedirs(destination_dir)
    else:
        print(f"Destination directory already exists: {destination_dir}")

    # Compile each Python file in the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.py'):
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_dir)
                target_dir = os.path.join(destination_dir)
                print(target_dir)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                target_file = os.path.join(target_dir, file + 'c')
                print(target_file)
                py_compile.compile(source_file, cfile=target_file)
                print(f"Compiled {source_file} to {target_file}")

destination_dir = os.environ.get('REMOTE_SCRIPTS_PATH')
compileTo(f'{destination_dir}/modulive','src/modulive/')
compileTo(f'{destination_dir}/modulive_wootingone','src/modulive_wootingone/')
compileTo(f'{destination_dir}/modulive_mft','src/modulive_mft/')

print("Compilation completed.")
