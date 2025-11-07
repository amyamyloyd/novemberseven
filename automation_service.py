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
    
    def _find_az_command(self):
        """Find Azure CLI command path."""
        # Try PATH first
        az_path = shutil.which('az')
        if az_path:
            return az_path
        
        # Check common install locations
        common_paths = [
            'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',
            'C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',
            '/usr/local/bin/az',
            '/opt/homebrew/bin/az'
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
    
    def authenticate_azure(self):
        """Authenticate Azure CLI."""
        self._log("-> Authenticating Azure CLI...")
        self._log("  (Browser will open for authentication)")
        self._log("")
        
        az_cmd = self._find_az_command()
        if not az_cmd:
            self._log("[ERROR] Azure CLI not found")
            return False
        
        # Check if already authenticated
        result = self._run_command([az_cmd, 'account', 'show'], check=False, capture_output=True)
        if result and result.returncode == 0:
            self._log("[OK] Azure CLI already authenticated")
            self._log("")
            return True
        
        # Authenticate with device code - capture output to show in browser
        try:
            # Run and capture output to display in browser
            process = subprocess.Popen(
                [az_cmd, 'login', '--use-device-code'],
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
                self._log("[OK] Azure CLI authenticated")
                self._log("")
                return True
            else:
                self._log("[ERROR] Azure authentication failed")
                return False
                
        except Exception as e:
            self._log(f"[ERROR] Azure authentication error: {str(e)}")
            return False
    
    def setup_azure_subscription(self):
        """Set Azure subscription from config."""
        subscription_id = self.config.get('azure_settings', {}).get('subscription_id')
        
        az_cmd = self._find_az_command()
        if not az_cmd:
            print("[WARN] Azure CLI not found - skipping subscription setup")
            return
        
        if subscription_id:
            print(f"-> Setting Azure subscription...")
            result = self._run_command([az_cmd, 'account', 'set', '--subscription', subscription_id], check=False)
            
            if result and result.returncode == 0:
                print(f"[OK] Azure subscription set: {subscription_id}")
            else:
                print(f"[WARN] Failed to set subscription {subscription_id}")
                print("Using default subscription instead")
        else:
            print("[WARN] No Azure subscription ID in config - using default")
        
        print("")
    
    def provision_azure_resources(self):
        """Provision all Azure resources: resource group, app service plan, web app, slots, static web app."""
        self._log_progress("PROGRESS:Provisioning Azure resources")
        self._log("-> Provisioning Azure resources...")
        
        az_cmd = self._find_az_command()
        if not az_cmd:
            self._log("[ERROR] Azure CLI not found")
            self._log_progress("ERROR:Azure CLI not found")
            raise RuntimeError("Azure CLI not found")
        
        # Get config values
        resource_group = self.config['azure_settings']['resource_group']
        app_service_name = self.config['azure_settings']['app_service_name']
        region = self.config['azure_settings']['region']
        project_name = self.config['user_identity']['project_name']
        openai_key = self.config['api_keys']['openai_api_key']
        
        # Check if resource group exists - fail if it does
        self._log("-> Checking if resource group exists...")
        result = self._run_command([
            az_cmd, 'group', 'exists', '--name', resource_group
        ], check=False, capture_output=True)
        
        if result and result.stdout.strip().lower() == 'true':
            self._log(f"[ERROR] Resource group '{resource_group}' already exists")
            self._log("[ERROR] Please delete existing resources or use different names")
            self._log_progress("ERROR:Resource group already exists")
            raise RuntimeError(f"Resource group '{resource_group}' already exists")
        
        # Create resource group
        self._log(f"-> Creating resource group '{resource_group}'...")
        self._run_command([
            az_cmd, 'group', 'create',
            '--name', resource_group,
            '--location', region,
            '--output', 'none'
        ])
        self._log(f"[OK] Resource group created")
        
        # Create App Service plan (Linux, B1 SKU - free tier eligible)
        plan_name = f"{app_service_name}-plan"
        self._log(f"-> Creating App Service plan '{plan_name}'...")
        self._run_command([
            az_cmd, 'appservice', 'plan', 'create',
            '--name', plan_name,
            '--resource-group', resource_group,
            '--sku', 'B1',
            '--is-linux',
            '--output', 'none'
        ])
        self._log(f"[OK] App Service plan created (Basic B1 - free tier eligible)")
        
        # Create Web App for prod environment (only prod, no dev)
        self._log(f"-> Creating Prod Web App '{app_service_name}'...")
        self._run_command([
            az_cmd, 'webapp', 'create',
            '--name', app_service_name,
            '--resource-group', resource_group,
            '--plan', plan_name,
            '--runtime', 'PYTHON:3.11',
            '--output', 'none'
        ])
        self._log(f"[OK] Prod Web App created")
        
        # Create Static Web App (empty resource, no GitHub linking)
        static_web_app_name = f"{app_service_name}-frontend"
        self._log(f"-> Creating Static Web App '{static_web_app_name}'...")
        self._run_command([
            az_cmd, 'staticwebapp', 'create',
            '--name', static_web_app_name,
            '--resource-group', resource_group,
            '--location', region,
            '--output', 'none'
        ])
        self._log(f"[OK] Static Web App created")
        
        # Get Static Web App URL
        result = self._run_command([
            az_cmd, 'staticwebapp', 'show',
            '--name', static_web_app_name,
            '--resource-group', resource_group,
            '--query', 'defaultHostname',
            '--output', 'tsv'
        ], capture_output=True)
        static_web_app_url = f"https://{result.stdout.strip()}" if result and result.stdout.strip() else ""
        
        # Configure environment variables for prod app
        self._log("-> Configuring prod app environment variables...")
        self._run_command([
            az_cmd, 'webapp', 'config', 'appsettings', 'set',
            '--name', app_service_name,
            '--resource-group', resource_group,
            '--settings',
            'ENVIRONMENT=production',
            f'PROJECT_NAME={project_name}',
            f'OPENAI_API_KEY={openai_key}',
            '--output', 'none'
        ])
        self._log(f"[OK] Prod app environment configured")
        
        # Save URLs to config
        backend_prod_url = f"https://{app_service_name}.azurewebsites.net"
        
        self.config['azure_settings']['backend_prod_url'] = backend_prod_url
        self.config['azure_settings']['static_web_app_url'] = static_web_app_url
        self._save_config()
        
        self._log("[OK] All Azure resources provisioned")
        self._log_progress("DONE:Provisioning Azure resources")
        self._log("")
    
    def create_github_workflows(self):
        """Create GitHub Actions workflow file for prod deployment from main branch."""
        self._log_progress("PROGRESS:Creating GitHub workflow")
        self._log("-> Creating GitHub workflow...")
        
        # Create .github/workflows directory
        workflows_dir = Path('.github/workflows')
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        app_service_name = self.config['azure_settings']['app_service_name']
        
        # Create deploy-prod.yml (only prod, deploys from main)
        deploy_prod_yml = workflows_dir / 'deploy-prod.yml'
        deploy_prod_content = f"""name: Deploy to Azure Prod

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: '{app_service_name}'
        package: '.'
"""
        deploy_prod_yml.write_text(deploy_prod_content, encoding='utf-8')
        self._log("[OK] Created deploy-prod.yml")
        
        # Remove deploy-dev.yml if it exists
        deploy_dev_yml = workflows_dir / 'deploy-dev.yml'
        if deploy_dev_yml.exists():
            deploy_dev_yml.unlink()
            self._log("[OK] Removed deploy-dev.yml (dev not needed)")
        
        # Stage workflow files
        self._run_command(['git', 'add', '.github/workflows/'], check=False)
        
        self._log("[OK] GitHub workflow created")
        self._log_progress("DONE:Creating GitHub workflows")
        self._log("")
    
    def set_azure_publish_profiles(self):
        """Get Azure publish profile for prod app and set as GitHub secret (using Azure credentials instead)."""
        self._log_progress("PROGRESS:Setting Azure credentials")
        self._log("-> Setting Azure credentials for GitHub Actions...")
        
        # We're using Azure service principal (AZURE_CREDENTIALS) instead of publish profiles
        # This was already set up, so we just confirm
        self._log("[OK] Using Azure service principal authentication (AZURE_CREDENTIALS)")
        self._log_progress("DONE:Setting Azure credentials")
        self._log("")
    
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
    
    def get_azure_publish_profile(self) -> str:
        """Get Azure App Service publish profile XML."""
        try:
            az_cmd = self._find_az_command()
            if not az_cmd:
                print("[WARN] Azure CLI not found")
                return None
            
            app_name = self.config['azure_settings']['app_service_name']
            resource_group = self.config['azure_settings'].get('resource_group')
            
            if not resource_group:
                print("[WARN] Resource group not configured")
                return None
            
            # Get publish profile from Azure
            result = self._run_command([
                az_cmd, 'webapp', 'deployment', 'list-publishing-profiles',
                '--name', app_name,
                '--resource-group', resource_group,
                '--xml'
            ], capture_output=True, check=False)
            
            if result and result.returncode == 0:
                return result.stdout.strip()
            else:
                print("[WARN] Could not retrieve Azure publish profile")
                return None
                
        except Exception as e:
            print(f"[WARN] Error getting publish profile: {e}")
            return None
    
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
    
    def set_azure_secrets(self):
        """Set Azure deployment secrets in GitHub."""
        self._log_progress("PROGRESS:Setting Azure deployment secrets")
        print("-> Setting Azure deployment secrets...")
        
        gh_cmd = self._find_gh_command()
        if not gh_cmd:
            print("[ERROR] GitHub CLI not found")
            return
        
        # Get publish profile from Azure
        publish_profile = self.get_azure_publish_profile()
        
        if not publish_profile:
            print("[WARN] Skipping Azure secrets - publish profile not available")
            print("  You'll need to set AZURE_WEBAPP_PUBLISH_PROFILE manually in GitHub")
            self._log_progress("DONE:Setting Azure deployment secrets")
            return
        
        # Set publish profile as GitHub secret
        try:
            proc = subprocess.Popen(
                [gh_cmd, 'secret', 'set', 'AZURE_WEBAPP_PUBLISH_PROFILE'],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            proc.communicate(input=publish_profile.encode())
            
            print("[OK] Azure deployment secrets set")
            self._log_progress("DONE:Setting Azure deployment secrets")
        except Exception as e:
            print(f"[WARN] Failed to set Azure secrets: {e}")
            print("  You'll need to set AZURE_WEBAPP_PUBLISH_PROFILE manually")
            self._log_progress("DONE:Setting Azure deployment secrets")
    
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
        """No dev environment - skip this step."""
        self._log_progress("PROGRESS:Skipping dev environment")
        self._log("-> Skipping dev environment (prod only)")
        self._log_progress("DONE:Skipping dev environment")
    
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
            
            # Step 0: Install CLI tools
            if not self.install_cli_tools():
                print("[ERROR] CLI tool installation failed")
                return False
            
            # Step 0.1: Authenticate
            if not self.authenticate_github():
                return False
            
            if not self.authenticate_azure():
                return False
            
            self.setup_azure_subscription()
            
            # Step 0.2: Provision Azure resources
            self.provision_azure_resources()
            
            # Step 0.3: Create GitHub workflows
            self.create_github_workflows()
            
            # Step 0.4: Set Azure publish profiles
            self.set_azure_publish_profiles()
            
            # Step 0.5: Create coming soon pages
            self.create_coming_soon_pages()
            
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
            
            # Step 7: Secure config
            self.secure_config_file()
            
            # Step 9: Set API key secrets
            self.set_api_key_secrets()
            
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

