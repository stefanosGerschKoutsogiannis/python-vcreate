# vcreate - Virtual Environment Creation Tool

`vcreate` is a command-line tool designed to simplify the creation of Python virtual environments and the installation of dependencies. It allows you to create a virtual environment, specify dependencies, and optionally scan a directory for additional dependencies.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
    * [Options](#options)
    * [Examples](#examples)
* [How it Works](#how-it-works)
* [Core Library Exclusion](#core-library-exclusion)
* [Error Handling](#error-handling)
* [Requirements](#requirements)
* [Contributing](#contributing)
* [License](#license)
* [Script Description](#script-description)
* [Detailed Functionality](#detailed-functionality)

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd vcreate
    ```
2.  **Make the Script Executable (Unix-like systems):**
    ```bash
    chmod +x vcreate.py
    ```
3.  **Add to PATH (Optional):**
    * To run `vcreate` from any directory, move `vcreate.py` to a directory in your system's PATH.
    * Alternatively, add the directory containing `vcreate.py` to your PATH environment variable.

# Usage

```bash
vcreate.py -f <FILEPATH> [-d <DEPENDENCIES>] [-s]
```

## Options

* `-f, --filepath <FILEPATH>`:
    * Required.
    * The path where the virtual environment will be created.
* `-d, --dependencies <DEPENDENCIES>`:
    * Optional.
    * A space-separated list of dependencies to install.
    * Example: `-d requests pandas numpy`
* `-s, --scan`:
    * Optional.
    * If present, the tool will scan the specified directory for Python files and extract import statements to identify additional dependencies.

## Examples

* **Create a virtual environment in the current directory, install `requests` and `pandas`, and scan for additional dependencies:**

    ```bash
    vcreate.py -f . -d requests pandas -s
    ```

* **Create a virtual environment in `/home/user/projects/my_project`, install only `flask`, and do not scan:**

    ```bash
    vcreate.py -f /home/user/projects/my_project -d flask
    ```

* **Create a virtual enviroment in the current directory, and scan for dependancies, but do not add any dependancies from the command line:**

    ```bash
    vcreate.py -f . -s
    ```
## How it Works

* **Virtual Environment Creation:**
    * The script uses `venv` to create a virtual environment in the specified `FILEPATH`.
* **Dependency Handling:**
    * If `-d` is provided, those dependencies are added to `requirements.txt`.
    * If `-s` is provided, the script scans Python files in the directory for `import` statements and adds those dependencies to `requirements.txt`.
    * Python core libraries are excluded from the `requirements.txt` file.
* **Installation:**
    * The script uses `pip` to install the dependencies listed in `requirements.txt`.
* **Activation:**
    * The script prints a message with the command to activate the virtual environment.
 
## Core Library Exclusion

* `vcreate` automatically excludes Python's core libraries from the dependency list, preventing unnecessary downloads.
* This ensures that only external dependencies are installed.

## Error Handling

* The script includes error handling for virtual environment creation, dependency installation, and file reading.
* It provides informative error messages to assist with troubleshooting.

## Requirements

* Python 3.6 or higher.
* `venv` module (usually included with Python).

## Contributing

Contributions are welcome! If you find a bug or have an idea for an enhancement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Script Description

`vcreate.py` is a Python script designed to streamline the process of creating virtual environments and managing dependencies. It simplifies the setup of Python projects by automating the creation of virtual environments and the installation of necessary packages.

## Detailed Functionality

* **Virtual Environment Creation:**
    * The script uses the `venv` module to create a virtual environment in the specified directory.
    * It handles platform-specific differences between Windows and Unix-like systems.
* **Dependency Scanning:**
    * If the `-s` flag is provided, the script scans Python files in the specified directory for `import` statements.
    * It uses regular expressions to extract module names from `import` and `from` statements.
    * Core python libraries are automatically excluded.
* **Dependency Installation:**
    * The script creates a `requirements.txt` file containing the specified and scanned dependencies.
    * It uses `pip` to install the dependencies from the `requirements.txt` file.
* **Error Handling:**
    * The script includes `try-except` blocks to handle potential errors during virtual environment creation, dependency scanning, and installation.
    * It provides informative error messages to the user.
* **Command-Line Arguments:**
    * The script uses `argparse` to handle command-line arguments, making it easy to specify the virtual environment directory, and dependencies.
* **Core Library Exclusion:**
    * The script uses the `pkgutil` module to get a list of core python libraries, and then excludes them from the `requirements.txt` file.
* **Readability:**
    * The code is well-structured and documented, making it easy to understand and maintain.
