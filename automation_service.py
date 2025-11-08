"""
Automation Service - Handles all setup automation in Python
Replaces external bash/PowerShell scripts for cross-platform compatibility
"""

import os
import sys
import json
import subprocess
import time
import platform
import shutil
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional


class AutomationService:
    """Handles automated setup and deployment."""
    
    def __init__(self, config_path: str = 'user_config.json'):
        self.config_path = config_path
        self.config = self._load_config()
        self.is_windows = platform.system() == 'Windows'
        self.progress_log = 'setup_progress.log'
        
    def _load_config(self) -> Dict[str, Any]:
        """Load user configuration."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_config(self):
        """Save updated configuration."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def _log(self, message: str):
        """Log message with timestamp to console and file."""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"[{timestamp}] {message}"
        print(formatted)
        with open(self.progress_log, 'a', encoding='utf-8') as f:
            f.write(f"{formatted}\n")
    
    def _log_progress(self, message: str):
        """Log progress to file (for /progress endpoint)."""
        with open(self.progress_log, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")
    
    def _run_command(self, cmd: list, check=True, capture_output=False) -> Optional[subprocess.CompletedProcess]:
        """Run shell command with error handling."""
        try:
            if capture_output:
                result = subprocess.run(cmd, check=check, capture_output=True, text=True, encoding='utf-8')
                return result
            else:
                result = subprocess.run(cmd, check=check, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return result
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Command failed: {' '.join(cmd)}")
            print(f"        {str(e)}")
            if not check:
                return None
            raise
        except FileNotFoundError:
            print(f"[ERROR] Command not found: {cmd[0]}")
            if not check:
                return None
            raise
    
    def _find_gh_command(self):
        """Find GitHub CLI command path."""
        # Try PATH first
        gh_path = shutil.which('gh')
        if gh_path:
            return gh_path
        
        # Check common install locations
        common_paths = [
            'C:\\Program Files\\GitHub CLI\\gh.exe',
            'C:\\Program Files (x86)\\GitHub CLI\\gh.exe',
            os.path.expanduser('~/bin/gh'),
            '/usr/local/bin/gh',
            '/opt/homebrew/bin/gh'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _find_gh_command(self):
        """Find GitHub CLI executable, refreshing PATH if needed."""
        # Try PATH first
        gh_path = shutil.which('gh')
        if gh_path:
            return gh_path
        
        # On Windows, refresh PATH from registry
        if self.is_windows:
            try:
                import winreg
                import time
                
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')
                path_value, _ = winreg.QueryValueEx(key, 'Path')
                winreg.CloseKey(key)
                os.environ['PATH'] = path_value
                time.sleep(1)  # Brief wait for PATH update
                
                # Try again after refresh
                gh_path = shutil.which('gh')
                if gh_path:
                    return gh_path
            except:
                pass
        
        # Check common installation paths
        common_paths = [
            r'C:\Program Files\GitHub CLI\gh.exe',
            r'C:\Program Files (x86)\GitHub CLI\gh.exe',
            '/usr/local/bin/gh',
            '/opt/homebrew/bin/gh'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _find_az_command(self):
        """Find Azure CLI executable, refreshing PATH if needed."""
        # Try PATH first
        az_path = shutil.which('az')
        if az_path:
            return az_path
        
        # On Windows, refresh PATH from registry
        if self.is_windows:
            try:
                import winreg
                import time
                
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')
                path_value, _ = winreg.QueryValueEx(key, 'Path')
                winreg.CloseKey(key)
                os.environ['PATH'] = path_value
                time.sleep(1)  # Brief wait for PATH update
                
                # Try again after refresh
                az_path = shutil.which('az')
                if az_path:
                    return az_path
            except:
                pass
        
        # Check common installation paths
        common_paths = [
            r'C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd',
            r'C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd',
            '/usr/local/bin/az',
            '/opt/homebrew/bin/az'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def install_cli_tools(self):
        """Verify CLI tools are installed (install_tools.py handles installation)."""
        self._log("==================================================")
        self._log("  [VERIFY] Checking CLI Tools")
        self._log("==================================================")
        self._log("")
        
        # Verify GitHub CLI
        gh_cmd = self._find_gh_command()
        if not gh_cmd:
            self._log("[ERROR] GitHub CLI (gh) not found")
            self._log("[ERROR] This should have been installed by welcome script")
            self._log_progress("ERROR:GitHub CLI not found")
            return False
        
        self._log("[OK] GitHub CLI found")
        self._log_progress("GitHub CLI verified")
        
        # Verify Azure CLI
        az_cmd = self._find_az_command()
        if not az_cmd:
            self._log("[ERROR] Azure CLI (az) not found")
            self._log("[ERROR] This should have been installed by welcome script")
            self._log_progress("ERROR:Azure CLI not found")
            return False
        
        self._log("[OK] Azure CLI found")
        self._log_progress("Azure CLI verified")
        
        self._log("")
        return True
    
    def authenticate_github(self):
        """Authenticate GitHub CLI."""
        self._log("-> Authenticating GitHub CLI...")
        self._log("  (Browser will open for authentication)")
        self._log("")
        
        gh_cmd = self._find_gh_command()
        if not gh_cmd:
            self._log("[ERROR] GitHub CLI not found")
            return False
        
        # Check if already authenticated
        result = self._run_command([gh_cmd, 'auth', 'status'], check=False, capture_output=True)
        if result and result.returncode == 0:
            self._log("[OK] GitHub CLI already authenticated")
            self._log("")
            return True
        
        # Authenticate with device code - capture output to show in browser
        try:
            # Run and capture output to display in browser
            process = subprocess.Popen(
                [gh_cmd, 'auth', 'login', '--web', '--git-protocol', 'https'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Stream output to browser in real-time
            for line in process.stdout:
                clean_line = line.rstrip()
                self._log(clean_line)
            
            process.wait()
            
            if process.returncode == 0:
                self._log("")
                self._log("[OK] GitHub CLI authenticated")
                self._log("")
                return True
            else:
                self._log("[ERROR] GitHub authentication failed")
                return False
                
        except Exception as e:
            self._log(f"[ERROR] GitHub authentication error: {str(e)}")
            return False
    
    def create_coming_soon_pages(self):
        """Create coming soon HTML page for prod environment."""
        self._log_progress("PROGRESS:Creating coming soon page")
        self._log("-> Creating coming soon page...")
        
        # Create templates directory
        templates_dir = Path('templates')
        templates_dir.mkdir(exist_ok=True)
        
        project_name = self.config['user_identity']['project_name']
        
        # Create coming-soon-prod.html (only prod)
        prod_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Production - Coming Soon</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-green-500 via-teal-500 to-blue-500 flex items-center justify-center">
    <div class="text-center px-4">
        <h1 class="text-6xl font-bold text-white mb-4">🚀 Coming Soon</h1>
        <h2 class="text-4xl font-semibold text-white mb-8">{project_name}</h2>
        <p class="text-xl text-white/90 max-w-md mx-auto">
            Your production app will be here soon! This is a temporary placeholder while deployment completes.
        </p>
    </div>
</body>
</html>
"""
        prod_file = templates_dir / 'coming-soon-prod.html'
        prod_file.write_text(prod_html, encoding='utf-8')
        self._log("[OK] Created coming-soon-prod.html")
        
        # Remove dev coming soon page if it exists
        dev_file = templates_dir / 'coming-soon-dev.html'
        if dev_file.exists():
            dev_file.unlink()
            self._log("[OK] Removed coming-soon-dev.html (dev not needed)")
        
        # Stage template files
        self._run_command(['git', 'add', 'templates/'], check=False)
        
        self._log("[OK] Coming soon page created")
        self._log_progress("DONE:Creating coming soon page")
        self._log("")
    
    def setup_git_remote(self):
        """Configure git remote."""
        github_url = self.config['git_deployment']['github_repo_url']
        
        print("-> Configuring git remote...")
        
        # Try to add remote
        result = self._run_command(['git', 'remote', 'add', 'origin', github_url], check=False)
        
        # If failed (already exists), update it
        if result and result.returncode != 0:
            self._run_command(['git', 'remote', 'set-url', 'origin', github_url], check=False)
        
        print(f"[OK] Git remote configured: {github_url}")
        print("")
    
    def create_virtual_environment(self):
        """Create Python virtual environment."""
        self._log_progress("PROGRESS:Creating virtual environment")
        print("-> Creating virtual environment...")
        
        if not os.path.exists('venv'):
            python_cmd = 'python' if self.is_windows else 'python3'
            self._run_command([python_cmd, '-m', 'venv', 'venv'])
        
        print("[OK] Virtual environment ready")
        self._log_progress("DONE:Creating virtual environment")
    
    def install_dependencies(self):
        """Install Python dependencies."""
        self._log_progress("PROGRESS:Installing dependencies")
        print("-> Installing dependencies...")
        
        # Get path to pip in venv
        if self.is_windows:
            pip_path = os.path.join('venv', 'Scripts', 'pip.exe')
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:
            pip_path = os.path.join('venv', 'bin', 'pip')
            python_path = os.path.join('venv', 'bin', 'python')
        
        # Upgrade pip
        self._run_command([python_path, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install requirements
        self._run_command([pip_path, 'install', '-r', 'requirements.txt'])
        
        print("[OK] Dependencies installed")
        self._log_progress("DONE:Installing dependencies")
    
    def initialize_database(self):
        """Initialize SQLite database."""
        self._log_progress("PROGRESS:Initializing database")
        print("-> Initializing database...")
        
        if self.is_windows:
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:
            python_path = os.path.join('venv', 'bin', 'python')
        
        self._run_command([python_path, 'database.py'])
        
        print("[OK] Database initialized")
        self._log_progress("DONE:Initializing database")
    
    def build_welcome_page(self):
        """Build React welcome page."""
        self._log_progress("PROGRESS:Building welcome page")
        print("-> Building welcome page...")
        
        user_name = self.config['user_identity']['user_name']
        project_name = self.config['user_identity']['project_name']
        github_url = self.config['git_deployment']['github_repo_url']
        
        # Create config.js for frontend
        config_js = f"""window.bootLangConfig = {{
  userName: "{user_name}",
  projectName: "{project_name}",
  githubUrl: "{github_url}"
}};
"""
        os.makedirs('frontend/public', exist_ok=True)
        with open('frontend/public/config.js', 'w', encoding='utf-8') as f:
            f.write(config_js)
        
        # Update index.html to include config.js
        index_html_path = 'frontend/public/index.html'
        if os.path.exists(index_html_path):
            with open(index_html_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            if 'config.js' not in html:
                html = html.replace('</head>', '  <script src="%PUBLIC_URL%/config.js"></script>\n  </head>')
                with open(index_html_path, 'w', encoding='utf-8') as f:
                    f.write(html)
        
        # Build React app
        os.chdir('frontend')
        self._run_command(['npm', 'install'])
        self._run_command(['npm', 'run', 'build'])
        os.chdir('..')
        
        print("[OK] Welcome page built")
        self._log_progress("DONE:Building welcome page")
    
    def secure_config_file(self):
        """Add user_config.json to .gitignore."""
        self._log_progress("PROGRESS:Securing configuration file")
        
        gitignore_path = '.gitignore'
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""
        
        if 'user_config.json' not in content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write("\nuser_config.json\n")
        
        self._log_progress("DONE:Securing configuration file")
    
    def set_api_key_secrets(self):
        """Set API key GitHub repository secrets."""
        self._log_progress("PROGRESS:Setting API key secrets")
        print("-> Setting API key secrets...")
        
        gh_cmd = self._find_gh_command()
        if not gh_cmd:
            print("[ERROR] GitHub CLI not found")
            return False
        
        openai_key = self.config['api_keys']['openai_api_key']
        anthropic_key = self.config['api_keys'].get('anthropic_api_key', '')
        langsmith_key = self.config['api_keys'].get('langsmith_api_key', '')
        
        # Set OpenAI key
        proc = subprocess.Popen([gh_cmd, 'secret', 'set', 'OPENAI_API_KEY'], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
        proc.communicate(input=openai_key.encode())
        
        # Set optional keys
        if anthropic_key:
            proc = subprocess.Popen([gh_cmd, 'secret', 'set', 'ANTHROPIC_API_KEY'], 
                                   stdin=subprocess.PIPE, 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
            proc.communicate(input=anthropic_key.encode())
        
        if langsmith_key:
            proc = subprocess.Popen([gh_cmd, 'secret', 'set', 'LANGSMITH_API_KEY'], 
                                   stdin=subprocess.PIPE, 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
            proc.communicate(input=langsmith_key.encode())
        
        print("[OK] API key secrets set")
        self._log_progress("DONE:Setting API key secrets")
    
    def commit_and_push(self):
        """Commit and push to GitHub."""
        self._log_progress("PROGRESS:Pushing to GitHub")
        print("-> Committing and pushing to GitHub...")
        
        project_name = self.config['user_identity']['project_name']
        
        # Ensure user_config.json is not staged (safety check)
        self._run_command(['git', 'reset', 'user_config.json'], check=False)
        self._run_command(['git', 'restore', '--staged', 'user_config.json'], check=False)
        
        # Add all files except user_config.json
        self._run_command(['git', 'add', '.'], check=False)
        self._run_command(['git', 'reset', 'user_config.json'], check=False)
        
        self._run_command(['git', 'commit', '-m', f'Initial Boot_Lang setup: {project_name}'], check=False)
        self._run_command(['git', 'push', '-u', 'origin', 'main', '--force'], check=False)
        
        print("[OK] Pushed to GitHub")
        self._log_progress("DONE:Pushing to GitHub")
    
    def cleanup(self):
        """Clean up after automation."""
        print("")
        # Kill setup server (will be done by the server itself)
        time.sleep(2)
    
    def start_helper_services(self):
        """Start all helper tools on high ports."""
        self._log_progress("PROGRESS:Starting helper services")
        print("")
        print("=" * 60)
        print("  [START] Launching Helper Tools")
        print("=" * 60)
        print("")
        
        # Start dashboard (port 9000)
        print("-> Starting dashboard on port 9000...")
        try:
            if self.is_windows:
                subprocess.Popen([
                    'start', 'cmd', '/k',
                    f'cd /d {os.getcwd()} && venv\\Scripts\\activate && python helper_server.py'
                ], shell=True)
            else:
                subprocess.Popen(['./venv/bin/python', 'helper_server.py'])
        except Exception as e:
            print(f"[ERROR] Failed to start dashboard: {e}")
            print("[INFO] Continuing with other services...")
        
        time.sleep(1)
        
        # Start PRD builder (port 9001)
        print("-> Starting PRD Builder on port 9001...")
        try:
            if self.is_windows:
                subprocess.Popen([
                    'start', 'cmd', '/k',
                    f'cd /d {os.getcwd()} && venv\\Scripts\\activate && python prd_builder.py'
                ], shell=True)
            else:
                subprocess.Popen(['./venv/bin/python', 'prd_builder.py'])
        except Exception as e:
            print(f"[ERROR] Failed to start PRD Builder: {e}")
            print("[INFO] Continuing with other services...")
        
        time.sleep(1)
        
        # Start admin panel (port 9002)
        print("-> Starting Admin Panel on port 9002...")
        try:
            if self.is_windows:
                subprocess.Popen([
                    'start', 'cmd', '/k',
                    f'cd /d {os.getcwd()} && venv\\Scripts\\activate && python admin_server.py'
                ], shell=True)
            else:
                subprocess.Popen(['./venv/bin/python', 'admin_server.py'])
        except Exception as e:
            print(f"[ERROR] Failed to start Admin Panel: {e}")
            print("[INFO] Continuing with other services...")
        
        time.sleep(2)
        
        # Open browser to dashboard
        try:
            webbrowser.open('http://localhost:9000')
        except Exception as e:
            print(f"[WARN] Could not open browser: {e}")
        
        print("[OK] Helper tools running:")
        print("  Dashboard:   http://localhost:9000")
        print("  PRD Builder: http://localhost:9001")
        print("  Admin Panel: http://localhost:9002")
        print("")
        
        self._log_progress("DONE:Starting helper services")
    
    def run_automation(self) -> bool:
        """Run full automation sequence."""
        try:
            # Initialize progress log
            with open(self.progress_log, 'w', encoding='utf-8') as f:
                f.write("Starting automation...\n")
            
            print("")
            print("==================================================")
            print("  Starting Automated Setup")
            print("==================================================")
            print("")
            
            # Step 0: Install CLI tools
            if not self.install_cli_tools():
                print("[ERROR] CLI tool installation failed")
                return False
            
            # Step 1: Authenticate GitHub
            if not self.authenticate_github():
                return False
            
            # Step 2: Setup git remote
            current_branch = self._run_command(['git', 'branch', '--show-current'], capture_output=True)
            if current_branch and current_branch.stdout.strip() != 'main':
                print(f"Switching from {current_branch.stdout.strip()} to main branch...")
                self._run_command(['git', 'checkout', 'main'])
            
            self.setup_git_remote()
            
            # Step 3: Create virtual environment
            self.create_virtual_environment()
            
            # Step 4: Install dependencies
            self.install_dependencies()
            
            # Step 5: Initialize database
            self.initialize_database()
            
            # Step 6: Secure config
            self.secure_config_file()
            
            # Step 7: Commit and push
            self.commit_and_push()
            
            # Step 8: Start helper services
            self.start_helper_services()
            
            print("")
            print("=" * 60)
            print("  [OK] Setup Complete!")
            print("=" * 60)
            print("")
            print("Your development environment is ready!")
            print("")
            print("📍 Helper Tools:")
            print("   Dashboard:   http://localhost:9000")
            print("   PRD Builder: http://localhost:9001")
            print("   Admin Panel: http://localhost:9002")
            print("")
            print("💡 Your app can use ports 3000, 8000, 8001, etc.")
            print("")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Automation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def run_automation(config_path: str = 'user_config.json') -> bool:
    """Main entry point for automation."""
    service = AutomationService(config_path)
    return service.run_automation()


if __name__ == '__main__':
    # Can be run standalone for testing
    success = run_automation()
    sys.exit(0 if success else 1)

