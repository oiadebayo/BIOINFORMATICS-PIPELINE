#!/usr/bin/env python3
import os
import json
import sys
from loguru import logger

def str_to_bool(value, default=False):
    if value is None:
        return default
    return value.lower() == "true"

def create_repository():
    try:
        import requests
    except ImportError:
        return {
            "success": False,
            "error": {"message": "The requests library is not installed."}
        }
    
    try:
        # Required parameter
        repo_name = os.getenv("REPOSITORY_NAME", "default_repo")
        
        # Optional parameters with defaults
        repo_description = os.getenv("REPOSITORY_DESCRIPTION", "This is your first repo!")
        repo_homepage = os.getenv("REPOSITORY_HOMEPAGE", "https://github.com")
        repo_private = str_to_bool(os.getenv("REPOSITORY_PRIVATE", "false"), False)
        repo_has_issues = str_to_bool(os.getenv("REPOSITORY_HAS_ISSUES", "true"), True)
        repo_has_projects = str_to_bool(os.getenv("REPOSITORY_HAS_PROJECTS", "true"), True)
        repo_has_wiki = str_to_bool(os.getenv("REPOSITORY_HAS_WIKI", "true"), True)
        repo_has_discussions = str_to_bool(os.getenv("REPOSITORY_HAS_DISCUSSIONS", "false"), False)
        
        team_id_str = os.getenv("REPOSITORY_TEAM_ID")
        repo_team_id = None
        
        repo_auto_init = str_to_bool(os.getenv("REPOSITORY_AUTO_INIT", "false"), False)
        gitignore_template = os.getenv("REPOSITORY_GITIGNORE_TEMPLATE", "")
        license_template = os.getenv("REPOSITORY_LICENSE_TEMPLATE", "")
        repo_allow_squash_merge = str_to_bool(os.getenv("REPOSITORY_ALLOW_SQUASH_MERGE", "true"), True)
        repo_allow_merge_commit = str_to_bool(os.getenv("REPOSITORY_ALLOW_MERGE_COMMIT", "true"), True)
        repo_allow_rebase_merge = str_to_bool(os.getenv("REPOSITORY_ALLOW_REBASE_MERGE", "true"), True)
        repo_allow_auto_merge = str_to_bool(os.getenv("REPOSITORY_ALLOW_AUTO_MERGE", "false"), False)
        repo_delete_branch_on_merge = str_to_bool(os.getenv("REPOSITORY_DELETE_BRANCH_ON_MERGE", "false"), False)
        squash_merge_commit_title = os.getenv("REPOSITORY_SQUASH_MERGE_COMMIT_TITLE", "PR_TITLE")
        squash_merge_commit_message = os.getenv("REPOSITORY_SQUASH_MERGE_COMMIT_MESSAGE", "PR_BODY")
        merge_commit_title = os.getenv("REPOSITORY_MERGE_COMMIT_TITLE", "PR_TITLE")
        merge_commit_message = os.getenv("REPOSITORY_MERGE_COMMIT_MESSAGE", "PR_BODY")
        repo_has_downloads = str_to_bool(os.getenv("REPOSITORY_HAS_DOWNLOADS", "true"), True)
        repo_is_template = str_to_bool(os.getenv("REPOSITORY_IS_TEMPLATE", "false"), False)
        
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise Exception("GITHUB_TOKEN is missing.")
        
        # Use the user repositories endpoint.
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        # Build the payload using the provided defaults and environment variables.
        payload = {
            "name": repo_name,
            "description": repo_description,
            "homepage": repo_homepage,
            "private": repo_private,
            "has_issues": repo_has_issues,
            "has_projects": repo_has_projects,
            "has_wiki": repo_has_wiki,
            "has_discussions": repo_has_discussions,
            "auto_init": repo_auto_init,
            "gitignore_template": gitignore_template if gitignore_template else None,
            "license_template": license_template if license_template else None,
            "allow_squash_merge": repo_allow_squash_merge,
            "allow_merge_commit": repo_allow_merge_commit,
            "allow_rebase_merge": repo_allow_rebase_merge,
            "allow_auto_merge": repo_allow_auto_merge,
            "delete_branch_on_merge": repo_delete_branch_on_merge,
            "squash_merge_commit_title": squash_merge_commit_title,
            "squash_merge_commit_message": squash_merge_commit_message,
            "merge_commit_title": merge_commit_title,
            "merge_commit_message": merge_commit_message,
            "has_downloads": repo_has_downloads,
            "is_template": repo_is_template
        }
        
        # Remove keys with None values from the payload.
        payload = {k: v for k, v in payload.items() if v is not None}
        
        # Include team_id only if provided.
        if repo_team_id is not None:
            payload["team_id"] = repo_team_id
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            logger.info("Repository '{}' created successfully.", repo_name)
            return {"success": True, "message": "it's ok", "repo": response.json()}
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
