import sys
import os
import subprocess
import platform
import re
import argparse
import pkgutil

def create_virtual_env(filepath, dependencies, scan_dependencies_flag):
    """
    Creates a virtual environment, optionally scans for dependencies, and installs them.

    Args:
        filepath (str): The path where the virtual environment should be created.
        dependencies (list): List of dependencies to install.
        scan_dependencies_flag (bool): if true, scan the given directory for additional dependencies.
    """

    os_name = platform.system()
    env_path = filepath

    try:
        pip_executable, activate_script = execute_command(os_name, env_path)
        print(f"Virtual environment created at: {env_path}")

        all_dependencies = list(dependencies) # make a copy to avoid unexpected behavior

        if scan_dependencies_flag:
            found_dependencies = scan_dependencies(filepath)
            all_dependencies.extend(found_dependencies)

        core_libraries = get_core_libraries()
        all_dependencies = [dep for dep in all_dependencies if dep not in core_libraries]       

        requirements_path = os.path.join(filepath, "requirements.txt")
        if all_dependencies:
            with open(requirements_path, "w") as f:
                for dep in set(all_dependencies): # remove duplicates and sort
                    f.write(dep + "\n")

            print(f"requirements.txt created at: {requirements_path}")
            subprocess.run([pip_executable, "install", "-r", requirements_path], check=True)
            print("Dependencies installed successfully.")
        else:
            print("No dependencies found. Skipping requirements.txt and installation.")

        print(f"To activate the virtual environment, run: '{activate_script}'")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def execute_command(os_name, env_path):
    """
    Executes the appropriate command to create a virtual environment based on the operating system.

    This function takes the operating system name and the desired virtual environment path as input.
    It then executes the 'venv' module using subprocess to create the virtual environment.
    It also determines the correct paths for the 'pip' executable and the 'activate' script,
    which vary depending on whether the operating system is Windows or a Unix-like system.

    Args:
        os_name (str): The name of the operating system (e.g., "Windows", "Linux", "Darwin").
        env_path (str): The path where the virtual environment should be created.

    Returns:
        tuple: A tuple containing the paths to the 'pip' executable and the 'activate' script.
               (pip_executable, activate_script)
    """
    if os_name == "Windows":
        subprocess.run([sys.executable, "-m", "venv", env_path], check=True)
        activate_script = os.path.join(env_path, "Scripts", "activate")
        pip_executable = os.path.join(env_path, "Scripts", "pip")
    else:
        subprocess.run([sys.executable, "-m", "venv", env_path], check=True)
        activate_script = os.path.join(env_path, "bin", "activate")
        pip_executable = os.path.join(env_path, "bin", "pip")
    
    return pip_executable, activate_script

def get_core_libraries():
    """
    Retrieves a list of Python's core libraries.

    Returns:
        list: A list of core library names.
    """
    core_libraries = [module.name for module in pkgutil.iter_modules()]
    #Filter out submodules.
    filtered_core_libraries = []
    for library in core_libraries:
        if "." not in library:
            filtered_core_libraries.append(library)

    return filtered_core_libraries

def scan_dependencies(filepath):
    """
    Scans Python files in the given filepath for import statements and extracts dependencies.

    Args:
        filepath (str): The path to scan for Python files.

    Returns:
        list: A list of unique dependencies found.
    """
    dependencies = set()
    for root, _, files in os.walk(filepath):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        imports = re.findall(r"import\s+([\w\d_]+)", content)
                        from_imports = re.findall(r"from\s+([\w\d_]+)", content)
                        dependencies.update(imports)
                        dependencies.update(from_imports)
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")

    filtered_dependencies = [dep for dep in dependencies if dep not in ['os', 'sys', 'math', 'random', 'datetime', 'json','re', 'typing', 'subprocess', 'platform','argparse']]

    return list(filtered_dependencies)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Creates a virtual environment and optionally installs dependencies.

        This script allows you to create a Python virtual environment in a specified directory.
        You can provide a list of dependencies to install, and optionally scan the directory
        for additional dependencies.
        """
    )
    parser.add_argument("-f", metavar="FILEPATH", help="Path to create the virtual environment.")
    parser.add_argument("-d", metavar="DEPENDENCIES", nargs="*", help="List of dependencies to install.")
    parser.add_argument(
        "-s",
        "--scan",
        action="store_true",
        help="Scan the directory for additional dependencies.",
    )

    args = parser.parse_args()

    # check if required arguments are present
    if not args.f:
        parser.print_help()
        sys.exit(1)

    create_virtual_env(args.f, args.d, args.scan)