# SaltAIr Welcome Email

**Subject:** Welcome to SaltAIr Dev OS - Your ideas, Built, Tested, Deployed

---

## HTML Email (Gmail/Yahoo Compatible)

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to SaltAIr</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f9fafb; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;">
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f9fafb; padding: 40px 20px;">
        <tr>
            <td align="center">
                <!-- Main Container -->
                <table cellpadding="0" cellspacing="0" border="0" width="600" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); padding: 30px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">Welcome to SaltAIr</h1>
                            <p style="margin: 8px 0 0; color: #e0e7ff; font-size: 14px;">Your ideas, Built, Tested, Deployed</p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            
                            <p style="margin: 0 0 30px; color: #374151; font-size: 16px; line-height: 1.6;">
                                Let's get you setup and building!
                            </p>
                            
                            <!-- Prerequisites Section -->
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 30px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h2 style="margin: 0 0 15px; color: #111827; font-size: 18px; font-weight: 600;">📋 Before You Start</h2>
                                        <p style="margin: 0 0 10px; color: #6b7280; font-size: 14px;">You'll need accounts on these platforms:</p>
                                        <ul style="margin: 0; padding-left: 20px; color: #6b7280; font-size: 14px; line-height: 1.8;">
                                            <li><strong>GitHub</strong> - Code repository (required)</li>
                                            <li><strong>Azure</strong> - Cloud hosting (required)</li>
                                            <li><strong>OpenAI</strong> - AI API (required)</li>
                                            <li><strong>Anthropic</strong> - Claude AI (optional)</li>
                                        </ul>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- GitHub -->
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h3 style="margin: 0 0 10px; color: #111827; font-size: 16px; font-weight: 600;">1. GitHub (Code Repository)</h3>
                                        <p style="margin: 0 0 15px; color: #6b7280; font-size: 14px; line-height: 1.6;">
                                            <strong>What it does:</strong> Git saves every change to your code. GitHub hosts it online so you can deploy apps.
                                        </p>
                                        <p style="margin: 0 0 10px; color: #374151; font-size: 14px;">
                                            <strong>Create account:</strong> <a href="https://github.com/signup" style="color: #6366f1; text-decoration: none;">github.com/signup →</a>
                                        </p>
                                        <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Then create your target repository:</p>
                                        <ol style="margin: 0 0 15px; padding-left: 20px; color: #6b7280; font-size: 14px; line-height: 1.8;">
                                            <li>Click "New repository" (green button)</li>
                                            <li>Name it: "my-app" or "project-name" (lowercase, hyphens okay)</li>
                                            <li>Set to <strong>PRIVATE</strong></li>
                                            <li>Don't add README/gitignore/license (leave empty)</li>
                                            <li>Click "Create repository"</li>
                                            <li>Copy the URL (https://github.com/username/repo-name)</li>
                                        </ol>
                                        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; border-radius: 4px;">
                                            <tr>
                                                <td style="color: #92400e; font-size: 13px;">
                                                    💡 <strong>Keep handy:</strong> Your GitHub username and password (you'll login during setup)
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Azure -->
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h3 style="margin: 0 0 10px; color: #111827; font-size: 16px; font-weight: 600;">2. Azure (Cloud Hosting)</h3>
                                        <p style="margin: 0 0 15px; color: #6b7280; font-size: 14px; line-height: 1.6;">
                                            <strong>What it does:</strong> Azure is Microsoft's cloud service that hosts your app online 24/7 so anyone can access it. SaltAIr will create all resources automatically - you just provide access.
                                        </p>
                                        <p style="margin: 0 0 10px; color: #374151; font-size: 14px;">
                                            <strong>Create account:</strong> <a href="https://portal.azure.com" style="color: #6366f1; text-decoration: none;">portal.azure.com →</a> (free tier includes $200 credit)
                                        </p>
                                        <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Get your Subscription ID:</p>
                                        <ol style="margin: 0 0 15px; padding-left: 20px; color: #6b7280; font-size: 14px; line-height: 1.8;">
                                            <li>Login to portal.azure.com</li>
                                            <li>Click "Subscriptions" in left menu</li>
                                            <li>Copy your Subscription ID (format: 12345678-1234-1234-1234-123456789abc)</li>
                                        </ol>
                                        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; border-radius: 4px;">
                                            <tr>
                                                <td style="color: #92400e; font-size: 13px;">
                                                    💡 <strong>Keep handy:</strong> Your Azure email and password (you'll login during setup)
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- OpenAI -->
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h3 style="margin: 0 0 10px; color: #111827; font-size: 16px; font-weight: 600;">3. OpenAI (AI API)</h3>
                                        <p style="margin: 0 0 10px; color: #374151; font-size: 14px;">
                                            <strong>Create account:</strong> <a href="https://platform.openai.com/signup" style="color: #6366f1; text-decoration: none;">platform.openai.com/signup →</a>
                                        </p>
                                        <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Get API key:</p>
                                        <ol style="margin: 0 0 15px; padding-left: 20px; color: #6b7280; font-size: 14px; line-height: 1.8;">
                                            <li>Go to platform.openai.com/api-keys</li>
                                            <li>Click "Create new secret key"</li>
                                            <li>Copy it immediately (you won't see it again)</li>
                                            <li>Add billing ($5 minimum) at platform.openai.com/settings/organization/billing</li>
                                        </ol>
                                        <p style="margin: 0; color: #dc2626; font-size: 13px; font-weight: 600;">
                                            ⚠️ Required for SaltAIr to work
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Anthropic (Optional) -->
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 30px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h3 style="margin: 0 0 10px; color: #111827; font-size: 16px; font-weight: 600;">4. Anthropic (Optional - Claude AI)</h3>
                                        <p style="margin: 0; color: #6b7280; font-size: 14px;">
                                            <strong>Create account:</strong> <a href="https://console.anthropic.com" style="color: #6366f1; text-decoration: none;">console.anthropic.com →</a><br>
                                            <strong>Get API key:</strong> console.anthropic.com/settings/keys
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Divider -->
                            <div style="height: 1px; background-color: #e5e7eb; margin: 30px 0;"></div>
                            
                            <!-- Step 1: Install Cursor -->
                            <h2 style="margin: 0 0 15px; color: #111827; font-size: 20px; font-weight: 600;">🚀 Step 1: Install Cursor</h2>
                            <p style="margin: 0 0 15px; color: #374151; font-size: 14px; line-height: 1.6;">
                                Download Cursor IDE (VS Code with AI built-in):
                            </p>
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 30px;">
                                <tr>
                                    <td>
                                        <a href="https://cursor.com/download" style="display: inline-block; background-color: #6366f1; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px;">Download Cursor →</a>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Step 2: Clone -->
                            <h2 style="margin: 0 0 15px; color: #111827; font-size: 20px; font-weight: 600;">🚀 Step 2: Clone SaltAIr</h2>
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 4px; margin-bottom: 15px;">
                                <tr>
                                    <td style="color: #92400e; font-size: 13px; font-weight: 600;">
                                        ⚠️ First: Check your email for GitHub repository invitation and click "Accept invitation"
                                    </td>
                                </tr>
                            </table>
                            <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Then in Cursor:</p>
                            <ol style="margin: 0 0 30px; padding-left: 20px; color: #6b7280; font-size: 14px; line-height: 1.8;">
                                <li>Click "Clone Git Repository" button</li>
                                <li>Paste: <code style="background-color: #f3f4f6; padding: 2px 6px; border-radius: 3px; font-family: monospace; color: #111827;">https://github.com/amyamyloyd/boot_lang</code></li>
                                <li>Choose folder to save it</li>
                                <li>Click "Open"</li>
                            </ol>
                            
                            <!-- New Step 3: Install Python & Git -->
                            <h2 style="margin: 0 0 15px; color: #111827; font-size: 20px; font-weight: 600;">🚀 Step 3: Install Python & Git</h2>
                            <p style="margin: 0 0 15px; color: #374151; font-size: 14px; line-height: 1.6;">
                                SaltAIr requires Python 3.11+ and Git for Windows.
                            </p>
                            
                            <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Install Python (in Cursor terminal):</p>
                            <pre style="background-color: #f3f4f6; padding: 10px; border-radius: 6px; margin: 0 0 10px; overflow-x: auto;"><code style="font-family: monospace; font-size: 13px; color: #111827;">winget install Python.Python.3.12</code></pre>
                            <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Verify Python:</p>
                            <pre style="background-color: #f3f4f6; padding: 10px; border-radius: 6px; margin: 0 0 20px; overflow-x: auto;"><code style="font-family: monospace; font-size: 13px; color: #111827;">python --version</code></pre>
                            
                            <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Install Git for Windows:</p>
                            <pre style="background-color: #f3f4f6; padding: 10px; border-radius: 6px; margin: 0 0 10px; overflow-x: auto;"><code style="font-family: monospace; font-size: 13px; color: #111827;">winget install Git.Git</code></pre>
                            <p style="margin: 0 0 10px; color: #374151; font-size: 14px; font-weight: 600;">Verify Git:</p>
                            <pre style="background-color: #f3f4f6; padding: 10px; border-radius: 6px; margin: 0 0 15px; overflow-x: auto;"><code style="font-family: monospace; font-size: 13px; color: #111827;">git --version</code></pre>
                            
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 12px; border-radius: 4px; margin-bottom: 30px;">
                                <tr>
                                    <td style="color: #991b1b; font-size: 13px; font-weight: 600;">
                                        ⚠️ CRITICAL: Both Python 3.11+ and Git are required. The setup will fail without Git Bash. Restart Cursor after installation.
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Step 4: Run Setup -->
                            <h2 style="margin: 0 0 15px; color: #111827; font-size: 20px; font-weight: 600;">🚀 Step 4: Run Setup</h2>
                            <p style="margin: 0 0 15px; color: #374151; font-size: 14px; line-height: 1.6;">
                                In Cursor, tell the AI agent:
                            </p>
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f3f4f6; border-radius: 6px; padding: 15px; margin-bottom: 30px;">
                                <tr>
                                    <td style="color: #111827; font-family: monospace; font-size: 14px; text-align: center;">
                                        "Run the welcome script"
                                    </td>
                                </tr>
                            </table>
                            <p style="margin: 0 0 30px; color: #6b7280; font-size: 14px;">
                                A setup form will open in your browser.
                            </p>
                            
                            <!-- Form Fields -->
                            <h2 style="margin: 0 0 15px; color: #111827; font-size: 20px; font-weight: 600;">📝 Fill Out the Form</h2>
                            <p style="margin: 0 0 15px; color: #374151; font-size: 14px; font-weight: 600;">Have these ready:</p>
                            <ul style="margin: 0 0 20px; padding-left: 20px; color: #6b7280; font-size: 14px; line-height: 1.8;">
                                <li>Your name & project name</li>
                                <li>GitHub repo URL (from step 1 above)</li>
                                <li>Azure Subscription ID (from step 2 above)</li>
                                <li>Azure Resource Group name (pick any, like "my-app-rg")</li>
                                <li>App Service name (must be globally unique, like "myapp-backend-2024")</li>
                                <li>OpenAI API key</li>
                                <li>Anthropic API key (optional)</li>
                            </ul>
                            
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #dbeafe; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                                <tr>
                                    <td style="color: #1e3a8a; font-size: 13px; line-height: 1.6;">
                                        <strong>During setup, browsers will open to login:</strong><br>
                                        • GitHub authentication<br>
                                        • Azure authentication<br><br>
                                        Keep your passwords handy!
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 0 0 30px; color: #374151; font-size: 14px;">
                                Click <strong>"Complete Setup"</strong> and wait 15-20 minutes while everything builds.
                            </p>
                            
                            <!-- What You Get -->
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f0fdf4; border: 1px solid #86efac; border-radius: 8px; margin-bottom: 30px;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <h2 style="margin: 0 0 15px; color: #166534; font-size: 18px; font-weight: 600;">✅ What You'll Get</h2>
                                        <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 14px; line-height: 1.8;">
                                            <li>Local development environment (React + FastAPI + SQLite)</li>
                                            <li>Production site deployed to Azure</li>
                                            <li>Development site deployed to Azure</li>
                                            <li>System dashboard to monitor deployments</li>
                                            <li>PRD Builder to create apps with AI</li>
                                        </ul>
                                        <p style="margin: 15px 0 0; color: #166534; font-size: 14px; font-weight: 600;">
                                            Your first login: <a href="http://localhost:3000" style="color: #6366f1; text-decoration: none;">http://localhost:3000</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Troubleshooting -->
                            <h3 style="margin: 0 0 15px; color: #111827; font-size: 16px; font-weight: 600;">❓ Troubleshooting</h3>
                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 30px;">
                                <tr>
                                    <td>
                                        <p style="margin: 0 0 8px; color: #6b7280; font-size: 13px; line-height: 1.6;">
                                            <strong style="color: #374151;">Setup fails?</strong> Reply with the error message
                                        </p>
                                        <p style="margin: 0 0 8px; color: #6b7280; font-size: 13px; line-height: 1.6;">
                                            <strong style="color: #374151;">Can't clone repo?</strong> Make sure you accepted the GitHub invitation
                                        </p>
                                        <p style="margin: 0 0 8px; color: #6b7280; font-size: 13px; line-height: 1.6;">
                                            <strong style="color: #374151;">Azure subscription not found?</strong> Complete billing setup in Azure Portal
                                        </p>
                                        <p style="margin: 0 0 8px; color: #6b7280; font-size: 13px; line-height: 1.6;">
                                            <strong style="color: #374151;">Questions?</strong> Reply to this email
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Footer Message -->
                            <p style="margin: 0; color: #374151; font-size: 16px; font-weight: 600;">
                                Happy building! 🚀
                            </p>
                            <p style="margin: 10px 0 0; color: #6b7280; font-size: 14px;">
                                - The SaltAIr Team
                            </p>
                            
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                            <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                SaltAIr v1.0 · Powered by Cursor AI
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

---

## Plain Text Version (Fallback)

```
Hi there,

Welcome to SaltAIr! Let's get you set up to build, test, and deploy apps with AI.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 BEFORE YOU START

You'll need accounts on these platforms:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. GITHUB (CODE REPOSITORY)

What it does: Git saves every change to your code. GitHub hosts it online so you can deploy apps.

Create account: https://github.com/signup

Then create your target repository:
1. Click "New repository" (green button)
2. Name it: "my-app" or "project-name" (lowercase, hyphens okay)
3. Set to PRIVATE
4. Don't add README/gitignore/license (leave empty)
5. Click "Create repository"
6. Copy the URL (https://github.com/username/repo-name)

💡 Keep handy: Your GitHub username and password (you'll login during setup)

Learn more: https://docs.github.com/en/get-started

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. AZURE (CLOUD HOSTING)

What it does: Azure is Microsoft's cloud service that hosts your app online 24/7 so anyone can access it. SaltAIr will create all resources automatically - you just provide access.

Create account: https://portal.azure.com (free tier includes $200 credit)

Get your Subscription ID:
1. Login to portal.azure.com
2. Click "Subscriptions" in left menu
3. Copy your Subscription ID (format: 12345678-1234-1234-1234-123456789abc)

💡 Keep handy: Your Azure email and password (you'll login during setup)

Learn more: https://azure.microsoft.com/free

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. OPENAI (AI API)

Create account: https://platform.openai.com/signup

Get API key:
1. Go to platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy it immediately (you won't see it again)
4. Add billing ($5 minimum) at platform.openai.com/settings/organization/billing

⚠️ Required for SaltAIr to work

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. ANTHROPIC (OPTIONAL - CLAUDE AI)

Create account: https://console.anthropic.com
Get API key: console.anthropic.com/settings/keys

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 STEP 1: INSTALL CURSOR

Download: https://cursor.com/download

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 STEP 2: CLONE SALTAIR

⚠️ First: Check your email for GitHub repository invitation and click "Accept invitation"

Then in Cursor:
1. Click "Clone Git Repository" button
2. Paste: https://github.com/amyamyloyd/boot_lang
3. Choose folder to save it
4. Click "Open"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 STEP 3: RUN SETUP

In Cursor, tell the AI agent:

   "Run the welcome script"

A setup form will open in your browser.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 FILL OUT THE FORM

Have these ready:

✓ Your name & project name
✓ GitHub repo URL (from GitHub section above)
✓ Azure Subscription ID (from Azure section above)
✓ Azure Resource Group name (pick any, like "my-app-rg")
✓ App Service name (must be globally unique, like "myapp-backend-2024")
✓ OpenAI API key
✓ Anthropic API key (optional)

During setup, browsers will open for:
• GitHub login
• Azure login

Keep your passwords handy!

Click "Complete Setup" and wait 15-20 minutes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ WHAT YOU'LL GET

After setup completes:

• Local development environment (React + FastAPI + SQLite)
• Production site deployed to Azure
• Development site deployed to Azure
• System dashboard to monitor deployments
• PRD Builder to create apps with AI

Your first login: http://localhost:3000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ TROUBLESHOOTING

Setup fails? Reply with the error message

Can't clone repo? Make sure you accepted the GitHub invitation

Azure subscription not found? Complete billing setup in Azure Portal

Questions? Reply to this email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Happy building! 🚀

- The SaltAIr Team
```

---

## Usage Instructions

**To send this email:**

1. Copy HTML version above
2. Use email service that supports HTML (SendGrid, Mailgun, Gmail API)
3. Subject: "Welcome to SaltAIr Dev OS - Your ideas, Built, Tested, Deployed"
4. Include plain text version as fallback

**Tested for compatibility:**
- Gmail (desktop & mobile)
- Yahoo Mail
- Outlook.com
- Apple Mail
- Mobile email clients

**Design features:**
- Inline styles (no external CSS)
- Table-based layout (email client safe)
- Gradient header
- Color-coded sections
- Clear call-to-action buttons
- Mobile responsive (600px max width)

