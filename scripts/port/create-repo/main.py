#!/usr/bin/env python3
import os
import json
import sys
from loguru import logger

def create_repository():
    try:
        import requests
    except ImportError:
        return {
            "success": False,
            "error": {"message": "The requests library is not installed."}
        }
    
    try:
        repo_name = os.getenv("REPOSITORY_NAME", "default_repo")
        owner_team = os.getenv("OWNER_TEAM", "default_team")
        default_branch = os.getenv("DEFAULT_BRANCH", "main")
        github_token = os.getenv("GITHUB_TOKEN")
        
        if not github_token:
            raise Exception("GITHUB_TOKEN is missing.")
        
        url = f"https://api.github.com/orgs/{owner_team}/repos"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github+json"
        }
        payload = {"name": repo_name, "auto_init": True}
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            logger.info("Repository '{}' created successfully.", repo_name)
            return {"success": True, "message": "it's ok"}
        else:
            try:
                error_data = response.json()
            except Exception:
                error_data = {
                    "message": "Repository creation failed",
                    "status": response.status_code
                }
            logger.error("Error creating repository: {}", error_data)
            return {"success": False, "error": error_data}
    except Exception as e:
        logger.exception("An exception occurred during repository creation.")
        return {"success": False, "error": {"message": str(e)}}

def main():
    result = create_repository()
    sys.stdout.write(json.dumps(result))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
