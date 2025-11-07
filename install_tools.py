"""
Tool Installation Checker
Verifies and installs required CLI tools before setup begins
"""

import subprocess
import sys
import platform
import shutil
from datetime import datetime
from pathlib import Path


class ToolInstaller:
    """Handles installation of required CLI tools."""
    
    def __init__(self):
        self.is_windows = platform.system() == 'Windows'
        self.log_file = 'setup_progress.log'
        self.required_tools = {
            'python': 'Python 3.11+',
            'git': 'Git',
            'gh': 'GitHub CLI',
            'az': 'Azure CLI'
        }
        
    def log(self, message):
        """Log message with timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"[{timestamp}] {message}"
        print(formatted)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{formatted}\n")
    
    def check_tool(self, command):
        """Check if a command is available in PATH."""
        return shutil.which(command) is not None
    
    def install_windows_tool(self, tool_name, winget_id):
        """Install tool via winget on Windows."""
        self.log(f"-> Installing {tool_name} via winget...")
        try:
            # Run WITHOUT --silent so UAC prompts appear
            result = subprocess.run(
                ['winget', 'install', '-e', '--id', winget_id],
                capture_output=False,  # Show output to user
                text=True
            )
            
            if result.returncode == 0:
                self.log(f"[OK] {tool_name} installed successfully")
                return True
            else:
                self.log(f"[WARN] {tool_name} installation returned code {result.returncode}")
                return False
                
        except Exception as e:
            self.log(f"[ERROR] Failed to install {tool_name}: {e}")
            return False
    
    def check_and_install(self):
        """Check for missing tools and install them."""
        self.log("=================================================")
        self.log("  [CHECK] Verifying Required Tools")
        self.log("=================================================")
        self.log("")
        
        missing_tools = []
        tools_installed = False
        
        # Check each tool
        for cmd, name in self.required_tools.items():
            if self.check_tool(cmd):
                self.log(f"[OK] {name} found")
            else:
                self.log(f"[WARN] {name} not found in PATH")
                missing_tools.append((cmd, name))
        
        if not missing_tools:
            self.log("")
            self.log("[OK] All required tools are installed")
            return 0  # Success, no restart needed
        
        # Install missing tools (Windows only, via winget)
        if self.is_windows:
            self.log("")
            self.log(f"-> Installing {len(missing_tools)} missing tool(s)...")
            self.log("   (You may see UAC prompts - please approve them)")
            self.log("")
            
            # Map commands to winget IDs
            winget_map = {
                'python': ('Python 3.12', 'Python.Python.3.12'),
                'git': ('Git', 'Git.Git'),
                'gh': ('GitHub CLI', 'GitHub.cli'),
                'az': ('Azure CLI', 'Microsoft.AzureCLI')
            }
            
            for cmd, name in missing_tools:
                if cmd in winget_map:
                    tool_name, winget_id = winget_map[cmd]
                    if self.install_windows_tool(tool_name, winget_id):
                        tools_installed = True
            
            if tools_installed:
                self.log("")
                self.log("[OK] Tool installation complete")
                self.log("-> Shell restart required to update PATH")
                return 1  # Success, restart needed
            else:
                self.log("")
                self.log("[ERROR] Some tools failed to install")
                self.log("Please install manually and re-run setup")
                return 2  # Failure
        else:
            # Mac/Linux - provide manual install instructions
            self.log("")
            self.log("[ERROR] Missing tools on Mac/Linux")
            self.log("Please install manually:")
            for cmd, name in missing_tools:
                if cmd == 'gh':
                    self.log(f"  - {name}: brew install gh")
                elif cmd == 'az':
                    self.log(f"  - {name}: brew install azure-cli")
                elif cmd == 'git':
                    self.log(f"  - {name}: brew install git")
            return 2  # Failure


if __name__ == "__main__":
    installer = ToolInstaller()
    exit_code = installer.check_and_install()
    sys.exit(exit_code)

