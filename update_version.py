import subprocess
import re
import os

def get_git_version():
    try:
        # Get version from git
        # describe --tags matches annotated tags, --always falls back to commit sha
        cmd = ["git", "describe", "--tags", "--always", "--dirty"]
        version = subprocess.check_output(cmd).decode().strip()
        return version
    except subprocess.CalledProcessError:
        return "0.0.0-unknown"

def update_settings_file(version):
    file_path = "settings.py"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, "r") as f:
        content = f.read()
    
    # Regex to find VERSION = "..." or '...'
    # We want to replace valid python string assignment
    pattern = r'(VERSION\s*=\s*)(["\'])(.*?)(["\'])'
    
    # Function to replace group 3 with new version
    def replacer(match):
        return f'{match.group(1)}{match.group(2)}{version}{match.group(4)}'
        
    new_content = re.sub(pattern, replacer, content)

    if content != new_content:
        with open(file_path, "w") as f:
            f.write(new_content)
        print(f"Updated settings.py with version: {version}")
    else:
        print(f"settings.py already up to date ({version})")

if __name__ == "__main__":
    v = get_git_version()
    update_settings_file(v)
