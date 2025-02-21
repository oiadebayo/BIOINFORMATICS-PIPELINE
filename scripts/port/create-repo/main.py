#!/usr/bin/env python3
import os
import json
import sys

def create_repository():
    repo_name = os.getenv("REPOSITORY_NAME", "default_repo")
    owner_team = os.getenv("OWNER_TEAM", "default_team")
    autolink_key_prefix = os.getenv("AUTOLINK_KEY_PREFIX", "default_prefix")
    default_branch = os.getenv("DEFAULT_BRANCH", "main")
    
    # Simulate repository creation logic
    response = {
        "repo_name": repo_name,
        "owner_team": owner_team,
        "autolink_key_prefix": autolink_key_prefix,
        "default_branch": default_branch,
        "status": "success",
        "message": f"Repository '{repo_name}' created successfully on branch '{default_branch}'."
    }
    return response

def main():
    result = create_repository()
    output = json.dumps(result)  # Ensure single-line JSON output
    print(output)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
