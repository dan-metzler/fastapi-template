import os
import sys
import shutil
import subprocess
import time
import re
from urllib.request import urlopen
from pathlib import Path


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def run_command(cmd, check=True):
    """
    Run a system command safely with better error logging.
    Shows stdout/stderr if the command fails.
    """
    try:
        result = subprocess.run(
            cmd,
            check=check,
            shell=True,
            text=True,
            capture_output=True
        )
        # If you want to see output live, print it here
        if result.stdout:
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running command: {cmd}")
        if e.stdout:
            print(f"--- STDOUT ---\n{e.stdout.strip()}")
        if e.stderr:
            print(f"--- STDERR ---\n{e.stderr.strip()}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"\n❌ Command not found: {cmd}")
        sys.exit(1)

def ensure_python_version(min_version=(3, 13)):
    """
    Ensure the running Python interpreter is >= min_version.
    min_version should be a tuple like (3, 13).
    """
    if sys.version_info < min_version:
        raise RuntimeError(
            f"❌ Python {min_version[0]}.{min_version[1]} or higher is required. "
            f"❌ Current version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Python version OK: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} | SystemExecutablePath: {sys.executable}")

def display_banner():
    print(f"""
{bcolors.OKGREEN}    ____           __              _       __                       __      __     
   / __/___ ______/ /_____ _____  (_)     / /____  ____ ___  ____  / /___ _/ /____ 
  / /_/ __ `/ ___/ __/ __ `/ __ \\/ /_____/ __/ _ \\/ __ `__ \\/ __ \\/ / __ `/ __/ _ \\
 / __/ /_/ (__  ) /_/ /_/ / /_/ / /_____/ /_/  __/ / / / / / /_/ / / /_/ / /_/  __/
/_/  \\__,_/____/\\__/\\__,_/ .___/_/      \\__/\\___/_/ /_/ /_/ .___/_/\\__,_/\\__/\\___/ 
                        /_/                              /_/{bcolors.ENDC}                       
""")

def create_project(project_folderpath, project_name):
    
    start_time = time.time()

    ####################################################################
    # display banner, check python version installed, define root folder
    ####################################################################
    display_banner()
    print("=================================================================================")
    ensure_python_version()
    print("=================================================================================")
    print()


    clone_directory = Path.cwd()

    # input validation
    input_path = Path(project_folderpath)

    if not input_path.exists():
        sys.exit(f"The input project_folderpath does not exist: {project_folderpath}")
        
    if not re.match(r'^[A-Za-z0-9_-]+$', project_name):
      sys.exit("Error: project name can only contain letters, numbers, hyphens, and underscores. No spaces allowed.")

    print(f"{bcolors.BOLD}{bcolors.OKCYAN}Initialize Project{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} project_name   : {project_name}")
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} project_folder : {project_folderpath}")    
    os.chdir(project_folderpath)
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Set Current directory:", Path.cwd())


    root_folder = input_path

    project_root = root_folder / project_name

    ####################################################################
    # Step 1: Create virtual environment using uv
    ####################################################################

    run_command('uv init --bare')
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} project initialized via 'uv init --bare'")


    ####################################################################
    # Handle file copying
    ####################################################################
    print()
    print(f"{bcolors.BOLD}{bcolors.OKCYAN}Copying Folders & Files{bcolors.ENDC}")
    # Copy entire folder tree into new folder with the user's project name
    app_template_src_folder = clone_directory / "app_template"
    app_template_dst_folder = root_folder / project_name
    shutil.copytree(app_template_src_folder, app_template_dst_folder)
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Copied app_template folder")
    
    # Copy .vscode folder from template into the root of the project
    vscode_src_folder = clone_directory / ".vscode"
    vscode_dst_folder = root_folder / ".vscode" 
    shutil.copytree(vscode_src_folder, vscode_dst_folder, dirs_exist_ok=True)
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Copied .vscode folder")

    prettierrc_file_src = clone_directory / ".prettierrc"
    shutil.copy2(prettierrc_file_src, root_folder)
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Copied .prettierrc file")

    # Path to the .gitignore file
    gitignore_path = root_folder / ".gitignore"
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.egg-info/
.env
.venv/

# OS junk
.DS_Store
Thumbs.db

# Logs
*.log

# IDE
.vscode/
    """
    gitignore_path.write_text(gitignore_content, encoding="utf-8")
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Created .gitignore file")

    ####################################################################
    # Step 4: Install dependencies
    ####################################################################
    print()
    print(f"{bcolors.BOLD}{bcolors.OKCYAN}Installing Dependencies{bcolors.ENDC}")
    req_file = clone_directory / "requirements.txt"
    run_command(f"uv add -r {req_file}")
    
    print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} requirements.txt installed")

    ####################################################################
    # Download HTMX
    ####################################################################
    js_dir = project_root / "frontend" / "public" / "js"
    js_dir.mkdir(parents=True, exist_ok=True)

    htmx_path = js_dir / "htmx.min.js"
    try:
        with urlopen("https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js") as r:
            data = r.read()
            htmx_path.write_bytes(data)
        print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Downloaded htmx ({len(data)} bytes) -> {htmx_path}")
    except Exception as e:
        print(f"❌ Error: Failed to download htmx: {e}")

    ####################################################################
    # Download Bulma CSS
    ####################################################################
    css_dir = project_root / "frontend" / "public" / "css"
    css_dir.mkdir(parents=True, exist_ok=True)

    bulma_path = css_dir / "bulma.min.css"
    try:
        with urlopen("https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css") as r:
            data = r.read()
            bulma_path.write_bytes(data)
        print(f"{bcolors.OKGREEN}✔{bcolors.ENDC} Downloaded Bulma CSS ({len(data)} bytes) -> {bulma_path}")
    except Exception as e:
        print(f"❌ Error: Failed to download Bulma CSS: {e}")

    end_time = time.time()  # record end
    elapsed = end_time - start_time

    print()
    print(f"🎉 {bcolors.BOLD}{bcolors.OKGREEN}Project setup complete in {elapsed:.2f} seconds, check it out!{bcolors.ENDC} {bcolors.WARNING}->{bcolors.ENDC} {bcolors.BOLD}{bcolors.OKCYAN}{root_folder}{bcolors.ENDC}")
    print()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a new project")
    parser.add_argument("project_folderpath", help="Folder where the project will be created")
    parser.add_argument("project_name", help="Name of the project")
    args = parser.parse_args()
    # Call your function
    create_project(args.project_folderpath, args.project_name)


# Example Usage: 
# python create_project.py myapp