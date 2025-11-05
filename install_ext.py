import subprocess
import sys
import os
import platform
import shutil

def find_cursor_command():
    """Find cursor CLI command path"""
    # Try PATH first
    cursor_path = shutil.which('cursor')
    if cursor_path:
        return cursor_path
    
    # Try app bundle paths
    is_windows = platform.system() == 'Windows'
    
    if is_windows:
        # Windows paths
        possible_paths = [
            r"C:\Users\{}\AppData\Local\Programs\cursor\cursor.exe".format(os.getenv('USERNAME')),
            r"C:\Program Files\Cursor\cursor.exe",
            r"C:\Program Files (x86)\Cursor\cursor.exe"
        ]
    else:
        # Mac paths
        possible_paths = [
            "/Applications/Cursor.app/Contents/Resources/app/bin/cursor",
            os.path.expanduser("~/Applications/Cursor.app/Contents/Resources/app/bin/cursor")
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def install_cursor_extension(extension_id):
    """Install a Cursor extension via command line"""
    cursor_cmd = find_cursor_command()
    
    if not cursor_cmd:
        print("[ERROR] 'cursor' command not found")
        print("       Please ensure Cursor is installed")
        return False
    
    try:
        result = subprocess.run(
            [cursor_cmd, "--install-extension", extension_id],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"[OK] Installed {extension_id}")
            return True
        else:
            print(f"[ERROR] Failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Installation timed out")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    extension = "mechatroner.rainbow-csv"
    print(f"Installing {extension}...")
    success = install_cursor_extension(extension)
    sys.exit(0 if success else 1)