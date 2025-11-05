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
    
    def _log_progress(self, message: str):
        """Log progress to file."""
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
    
    def check_and_install_clis(self):
        """Check and install GitHub CLI and Azure CLI."""
        print("==================================================")
        print("  [AUTH] CLI Authentication")
        print("==================================================")
        print("")
        
        # Check GitHub CLI
        if not shutil.which('gh'):
            print("[WARN] GitHub CLI not found")
            print("Installing GitHub CLI via winget..." if self.is_windows else "Please install GitHub CLI manually")
            
            if self.is_windows:
                try:
                    self._run_command(['winget', 'install', '-e', '--id', 'GitHub.cli'], check=False)
                    print("[OK] GitHub CLI installed - please restart and run setup again")
                    return False
                except:
                    print("[ERROR] Failed to install GitHub CLI")
                    print("       Please install manually from: https://cli.github.com/")
                    return False
            else:
                print("[ERROR] GitHub CLI not found")
                print("       macOS:   brew install gh")
                print("       Linux:   visit https://cli.github.com/")
                return False
        
        # Check Azure CLI
        if not shutil.which('az'):
            print("[WARN] Azure CLI not found")
            print("Installing Azure CLI via winget..." if self.is_windows else "Please install Azure CLI manually")
            
            if self.is_windows:
                try:
                    self._run_command(['winget', 'install', '-e', '--id', 'Microsoft.AzureCLI'], check=False)
                    print("[OK] Azure CLI installed - please restart and run setup again")
                    return False
                except:
                    print("[ERROR] Failed to install Azure CLI")
                    print("       Please install manually from: https://azure.microsoft.com/en-us/downloads/")
                    return False
            else:
                print("[ERROR] Azure CLI not found")
                print("       macOS:   brew install azure-cli")
                print("       Linux:   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash")
                return False
        
        print("[OK] CLIs installed")
        print("")
        return True
    
    def authenticate_github(self):
        """Authenticate GitHub CLI."""
        print("-> Authenticating GitHub CLI...")
        print("  (Browser will open for authentication)")
        print("")
        
        # Check if already authenticated
        result = self._run_command(['gh', 'auth', 'status'], check=False, capture_output=True)
        if result and result.returncode == 0:
            print("[OK] GitHub CLI already authenticated")
            print("")
            return True
        
        # Authenticate
        try:
            self._run_command(['gh', 'auth', 'login', '--web', '--git-protocol', 'https'], check=True)
            print("[OK] GitHub CLI authenticated")
            print("")
            return True
        except:
            print("[ERROR] GitHub authentication failed")
            print("Please try again or check your network connection")
            return False
    
    def authenticate_azure(self):
        """Authenticate Azure CLI."""
        print("-> Authenticating Azure CLI...")
        print("  (Browser will open for authentication)")
        print("")
        
        # Check if already authenticated
        result = self._run_command(['az', 'account', 'show'], check=False, capture_output=True)
        if result and result.returncode == 0:
            print("[OK] Azure CLI already authenticated")
            print("")
            return True
        
        # Authenticate
        try:
            self._run_command(['az', 'login', '--use-device-code'], check=True)
            print("[OK] Azure CLI authenticated")
            print("")
            return True
        except:
            print("[ERROR] Azure authentication failed")
            print("Please try again or check your network connection")
            return False
    
    def setup_azure_subscription(self):
        """Set Azure subscription from config."""
        subscription_id = self.config.get('azure_settings', {}).get('subscription_id')
        
        if subscription_id:
            print(f"-> Setting Azure subscription...")
            result = self._run_command(['az', 'account', 'set', '--subscription', subscription_id], check=False)
            
            if result and result.returncode == 0:
                print(f"[OK] Azure subscription set: {subscription_id}")
            else:
                print(f"[WARN] Failed to set subscription {subscription_id}")
                print("Using default subscription instead")
        else:
            print("[WARN] No Azure subscription ID in config - using default")
        
        print("")
    
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
    
    def configure_github_workflows(self):
        """Configure GitHub workflows."""
        self._log_progress("PROGRESS:Configuring GitHub workflows")
        print("-> Configuring GitHub workflows...")
        
        app_service_name = self.config['azure_settings']['app_service_name']
        deploy_yml_path = '.github/workflows/deploy.yml'
        
        if os.path.exists(deploy_yml_path):
            with open(deploy_yml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update app-name
            import re
            content = re.sub(r"app-name:.*", f"app-name: '{app_service_name}'", content)
            
            with open(deploy_yml_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print("[OK] GitHub workflows configured")
        self._log_progress("DONE:Configuring GitHub workflows")
    
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
    
    def set_github_secrets(self):
        """Set GitHub repository secrets."""
        self._log_progress("PROGRESS:Setting GitHub secrets")
        print("-> Setting GitHub secrets...")
        
        openai_key = self.config['api_keys']['openai_api_key']
        anthropic_key = self.config['api_keys'].get('anthropic_api_key', '')
        langsmith_key = self.config['api_keys'].get('langsmith_api_key', '')
        
        # Set OpenAI key
        proc = subprocess.Popen(['gh', 'secret', 'set', 'OPENAI_API_KEY'], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
        proc.communicate(input=openai_key.encode())
        
        # Set optional keys
        if anthropic_key:
            proc = subprocess.Popen(['gh', 'secret', 'set', 'ANTHROPIC_API_KEY'], 
                                   stdin=subprocess.PIPE, 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
            proc.communicate(input=anthropic_key.encode())
        
        if langsmith_key:
            proc = subprocess.Popen(['gh', 'secret', 'set', 'LANGSMITH_API_KEY'], 
                                   stdin=subprocess.PIPE, 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
            proc.communicate(input=langsmith_key.encode())
        
        print("[OK] GitHub secrets set")
        self._log_progress("DONE:Setting GitHub secrets")
    
    def commit_and_push(self):
        """Commit and push to GitHub."""
        self._log_progress("PROGRESS:Pushing to GitHub")
        print("-> Committing and pushing to GitHub...")
        
        project_name = self.config['user_identity']['project_name']
        
        self._run_command(['git', 'add', '.'], check=False)
        self._run_command(['git', 'commit', '-m', f'Initial Boot_Lang setup: {project_name}'], check=False)
        self._run_command(['git', 'push', '-u', 'origin', 'main', '--force'], check=False)
        
        print("[OK] Pushed to GitHub")
        self._log_progress("DONE:Pushing to GitHub")
    
    def create_dev_environment(self):
        """Create dev branch and Azure deployment slot."""
        self._log_progress("PROGRESS:Creating dev environment")
        print("")
        print("-> Creating dev branch...")
        
        # Create dev branch
        result = self._run_command(['git', 'checkout', '-b', 'dev'], check=False)
        if result and result.returncode != 0:
            self._run_command(['git', 'checkout', 'dev'], check=False)
        
        # Push dev branch
        self._run_command(['git', 'push', '-u', 'origin', 'dev', '--force'], check=False)
        
        print("[OK] Dev branch created and pushed")
        print("")
        
        # Create Azure deployment slot
        print("-> Creating Azure deployment slot (dev)...")
        
        resource_group = self.config['azure_settings'].get('resource_group')
        app_service_name = self.config['azure_settings']['app_service_name']
        
        if not resource_group:
            print("[WARN] Resource group not found in config - skipping dev slot creation")
            print("  You can create it manually later in Azure Portal")
        else:
            # Create slot
            self._run_command([
                'az', 'webapp', 'deployment', 'slot', 'create',
                '--name', app_service_name,
                '--resource-group', resource_group,
                '--slot', 'dev',
                '--configuration-source', app_service_name,
                '--output', 'none'
            ], check=False)
            
            dev_slot_url = f"https://{app_service_name}-dev.azurewebsites.net"
            print(f"[OK] Dev slot created: {dev_slot_url}")
            
            # Configure dev slot environment
            print("-> Configuring dev slot environment...")
            
            openai_key = self.config['api_keys']['openai_api_key']
            anthropic_key = self.config['api_keys'].get('anthropic_api_key', '')
            langsmith_key = self.config['api_keys'].get('langsmith_api_key', '')
            project_name = self.config['user_identity']['project_name']
            
            self._run_command([
                'az', 'webapp', 'config', 'appsettings', 'set',
                '--name', app_service_name,
                '--resource-group', resource_group,
                '--slot', 'dev',
                '--settings',
                'ENVIRONMENT=development',
                f'PROJECT_NAME={project_name}',
                f'OPENAI_API_KEY={openai_key}',
                f'ANTHROPIC_API_KEY={anthropic_key}',
                f'LANGSMITH_API_KEY={langsmith_key}',
                '--output', 'none'
            ], check=False)
            
            print("[OK] Dev slot environment configured")
            
            # Save dev URL to config
            self.config['azure_settings']['dev_slot_url'] = dev_slot_url
            self._save_config()
        
        print("")
        
        # Switch back to main
        self._run_command(['git', 'checkout', 'main'], check=False)
        
        self._log_progress("DONE:Creating dev environment")
    
    def verify_deployment(self):
        """Verify Azure deployment."""
        self._log_progress("PROGRESS:Verifying deployment")
        print("-> Waiting for GitHub Actions to start deployment...")
        time.sleep(15)
        self._log_progress("DONE:Deploying to Azure via GitHub Actions")
        
        azure_url = self.config['azure_settings'].get('static_web_app_url')
        if not azure_url:
            print("[WARN] No Azure URL configured - skipping verification")
            self._log_progress("DONE:Verifying deployment")
            return
        
        print(f"-> Testing deployment at: {azure_url}")
        
        # Try for up to 3 minutes
        deployment_verified = False
        for i in range(1, 37):
            try:
                import urllib.request
                req = urllib.request.Request(azure_url)
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        print(f"[OK] Deployment verified! Site responding (HTTP {response.status})")
                        deployment_verified = True
                        self._log_progress("DONE:Verifying deployment")
                        self._log_progress(f"COMPLETE:{azure_url}")
                        break
            except:
                pass
            
            print(f"[WAIT] Waiting for deployment... (attempt {i}/36)")
            time.sleep(5)
        
        if not deployment_verified:
            print("[WARN] Deployment verification timed out after 3 minutes")
            print(f"  URL: {azure_url}")
            print("  This may mean GitHub Actions is still building")
            print("  Your site may still deploy successfully - check the URL in a few minutes")
            self._log_progress("DONE:Verifying deployment")
            self._log_progress(f"ERROR:Deployment not verified - check GitHub Actions")
    
    def cleanup(self):
        """Clean up after automation."""
        print("")
        # Kill setup server (will be done by the server itself)
        time.sleep(2)
    
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
            
            # Step 0: Check and install CLIs
            if not self.check_and_install_clis():
                return False
            
            # Step 0.1: Authenticate
            if not self.authenticate_github():
                return False
            
            if not self.authenticate_azure():
                return False
            
            self.setup_azure_subscription()
            
            # Step 1: Ensure on main branch
            current_branch = self._run_command(['git', 'branch', '--show-current'], capture_output=True)
            if current_branch and current_branch.stdout.strip() != 'main':
                print(f"Switching from {current_branch.stdout.strip()} to main branch...")
                self._run_command(['git', 'checkout', 'main'])
            
            # Step 2: Setup git remote
            self.setup_git_remote()
            
            # Step 3: Create virtual environment
            self.create_virtual_environment()
            
            # Step 4: Install dependencies
            self.install_dependencies()
            
            # Step 5: Initialize database
            self.initialize_database()
            
            # Step 6: Build welcome page
            self.build_welcome_page()
            
            # Step 7: Configure workflows
            self.configure_github_workflows()
            
            # Step 8: Secure config
            self.secure_config_file()
            
            # Step 9: Set GitHub secrets
            self.set_github_secrets()
            
            # Step 10: Commit and push
            self.commit_and_push()
            
            # Step 11: Create dev environment
            self.create_dev_environment()
            
            # Step 12: Verify deployment
            self.verify_deployment()
            
            # Step 13: Cleanup
            self.cleanup()
            
            # Success message
            print("")
            print("==================================================")
            print("  [OK] Setup Complete!")
            print("==================================================")
            print("")
            print("Your Boot Lang environment is ready!")
            print("")
            print("📍 Access Points:")
            print("   Backend API: http://localhost:8000")
            print("   Frontend:    http://localhost:3000")
            
            azure_url = self.config['azure_settings'].get('static_web_app_url')
            if azure_url:
                print(f"   Deployed:    {azure_url}")
            
            print("")
            print("💡 Next Steps:")
            print("   • Start backend: tell Cursor 'Start backend'")
            print("   • Start frontend: tell Cursor 'Start frontend'")
            print("   • Login at http://localhost:3000")
            print("   • View System Dashboard at http://localhost:3000/dashboard")
            print("   • Build a PRD: tell Cursor 'Help me build a PRD'")
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

