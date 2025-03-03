import os
import subprocess
import sys
from github import Github
from dotenv import load_dotenv
from pathlib import Path

def run_command(command, cwd=None, error_message="Command failed"):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e.stderr}")
        sys.exit(1)

def create_and_push_to_github(project_path, github_username, github_token, repo_name):
    """Create a new GitHub repository and push the local project to it."""
    # Load environment variables (optional, for storing sensitive data)
    load_dotenv()
    
    # Ensure project path exists
    project_path = Path(project_path)
    if not project_path.exists():
        print(f"Project path {project_path} does not exist.")
        sys.exit(1)

    # Initialize Git in the project directory
    print("Initializing Git repository...")
    run_command("git init", cwd=project_path)

    # Add all files to Git
    print("Adding files to Git...")
    run_command("git add .", cwd=project_path)

    # Commit changes
    print("Committing changes...")
    run_command('git commit -m "Initial commit"', cwd=project_path)

    # Authenticate with GitHub using PyGitHub
    g = Github(github_token)  # Use the token directly here
    user = g.get_user(github_username)

    # Create a new repository on GitHub
    print(f"Creating GitHub repository: {repo_name}...")
    try:
        repo = user.create_repo(repo_name)
    except Exception as e:
        print(f"Failed to create GitHub repository: {e}")
        sys.exit(1)

    # Set the remote origin and push to GitHub
    remote_url = f"https://{github_username}:{github_token}@github.com/{github_username}/{repo_name}.git"
    print("Setting remote origin and pushing to GitHub...")
    run_command(f"git remote add origin {remote_url}", cwd=project_path)
    run_command("git push -u origin main", cwd=project_path)

    print(f"Successfully pushed to GitHub repository: https://github.com/{github_username}/{repo_name}")

def main():
    # Configuration (load from environment variables or defaults)
    project_path = "arbitrage_system"  # Path to your project folder
    github_username = os.getenv("GITHUB_USERNAME", "your-github-username")  # Default if not set
    github_token = os.getenv("GITHUB_TOKEN")  # Load from environment variable
    repo_name = "arbitrage_system"  # Desired repository name

    # Check if GITHUB_TOKEN is set
    if not github_token:
        print("GitHub token not found. Please set GITHUB_TOKEN as a system environment variable or in a .env file.")
        sys.exit(1)

    # Check if GITHUB_USERNAME is set, otherwise prompt or fail
    if not github_username or github_username == "your-github-username":
        print("GitHub username not found. Please set GITHUB_USERNAME as a system environment variable or update the script.")
        sys.exit(1)

    # Create and push to GitHub
    create_and_push_to_github(project_path, github_username, github_token, repo_name)

if __name__ == "__main__":
    main()