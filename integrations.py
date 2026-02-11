"""
GitHub Integration Module
Sync projects with GitHub repositories for seamless IP protection
"""

import hashlib
import datetime
import re
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class GitHubUser:
    """GitHub user profile"""
    username: str
    user_id: int
    avatar_url: str
    email: Optional[str] = None
    wallet_address: Optional[str] = None


@dataclass
class Commit:
    """Git commit information"""
    sha: str
    message: str
    author: str
    timestamp: str
    files_changed: int
    additions: int
    deletions: int


@dataclass 
class Repository:
    """GitHub repository"""
    name: str
    owner: str
    url: str
    description: str
    language: str
    stars: int
    is_private: bool


class GitHubIntegration:
    """
    GitHub OAuth & API Integration
    
    Features:
    - OAuth authentication
    - Repository analysis
    - Commit history tracking
    - Contribution analysis
    - Automatic IP registration on push
    """
    
    API_BASE = "https://api.github.com"
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self._repos = {}
        self._commits = {}
        
    def authenticate_oauth(self, code: str) -> dict:
        """
        Complete OAuth flow with authorization code
        
        Production flow:
        1. Redirect user to GitHub OAuth
        2. User authorizes app
        3. GitHub redirects with code
        4. Exchange code for access token
        """
        # Simulated OAuth response
        return {
            "access_token": f"gho_{'x' * 36}",
            "token_type": "bearer",
            "scope": "repo,read:user"
        }
    
    def get_user(self) -> GitHubUser:
        """Get authenticated user profile"""
        return GitHubUser(
            username="demo_user",
            user_id=12345678,
            avatar_url="https://avatars.githubusercontent.com/u/12345678",
            email="user@example.com"
        )
    
    def list_repositories(self, page: int = 1) -> List[Repository]:
        """List user's repositories"""
        # Simulated repos
        return [
            Repository(
                name="awesome-project",
                owner="demo_user",
                url="https://github.com/demo_user/awesome-project",
                description="An innovative blockchain project",
                language="Python",
                stars=42,
                is_private=False
            ),
            Repository(
                name="hackathon-2026",
                owner="demo_user", 
                url="https://github.com/demo_user/hackathon-2026",
                description="MLH Hackathon submission",
                language="JavaScript",
                stars=15,
                is_private=True
            )
        ]
    
    def get_commits(self, repo: str, branch: str = "main") -> List[Commit]:
        """Get commit history for a repository"""
        # Simulated commit history
        return [
            Commit(
                sha="a1b2c3d4e5f6",
                message="Add core algorithm implementation",
                author="demo_user",
                timestamp=datetime.datetime.now().isoformat(),
                files_changed=5,
                additions=342,
                deletions=12
            ),
            Commit(
                sha="b2c3d4e5f6g7",
                message="Implement blockchain integration",
                author="collaborator",
                timestamp=datetime.datetime.now().isoformat(),
                files_changed=3,
                additions=156,
                deletions=23
            )
        ]
    
    def analyze_contributions(self, repo: str) -> dict:
        """
        Analyze contributor statistics for fair ownership split
        """
        commits = self.get_commits(repo)
        
        # Aggregate by author
        contributors = {}
        total_additions = 0
        
        for commit in commits:
            author = commit.author
            if author not in contributors:
                contributors[author] = {
                    "commits": 0,
                    "additions": 0,
                    "deletions": 0
                }
            contributors[author]["commits"] += 1
            contributors[author]["additions"] += commit.additions
            contributors[author]["deletions"] += commit.deletions
            total_additions += commit.additions
        
        # Calculate ownership percentages
        result = []
        for author, stats in contributors.items():
            percentage = (stats["additions"] / total_additions * 100) if total_additions > 0 else 0
            result.append({
                "author": author,
                "commits": stats["commits"],
                "lines_added": stats["additions"],
                "lines_removed": stats["deletions"],
                "ownership_percentage": round(percentage, 1)
            })
        
        return {
            "repository": repo,
            "total_commits": len(commits),
            "total_lines": total_additions,
            "contributors": sorted(result, key=lambda x: x["ownership_percentage"], reverse=True)
        }
    
    def get_repo_content(self, repo: str, path: str = "") -> dict:
        """Get repository content for analysis"""
        return {
            "type": "dir",
            "path": path,
            "contents": [
                {"name": "README.md", "type": "file", "size": 2048},
                {"name": "src", "type": "dir"},
                {"name": "main.py", "type": "file", "size": 4096}
            ]
        }
    
    def setup_webhook(self, repo: str, webhook_url: str) -> dict:
        """
        Setup webhook for automatic IP registration on push
        
        Events to track:
        - push: New commits
        - release: New releases
        - pull_request: Merged PRs
        """
        return {
            "id": 123456789,
            "url": webhook_url,
            "events": ["push", "release"],
            "active": True,
            "created_at": datetime.datetime.now().isoformat()
        }


class DevpostIntegration:
    """
    Devpost Hackathon Platform Integration
    
    Features:
    - Import hackathon submissions
    - Display BrainBlock badge
    - Sync team members
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    def get_submission(self, project_url: str) -> dict:
        """Get Devpost project details"""
        return {
            "title": "BrainBlock Demo Project",
            "tagline": "Protecting student IP with AI + Blockchain",
            "description": "An innovative system for...",
            "team": [
                {"name": "Alice", "role": "Developer"},
                {"name": "Bob", "role": "Designer"}
            ],
            "technologies": ["Python", "Algorand", "React"],
            "hackathon": "MLH Hackathon 2026",
            "submitted_at": datetime.datetime.now().isoformat()
        }
    
    def import_project(self, project_url: str) -> dict:
        """Import project for BrainBlock registration"""
        submission = self.get_submission(project_url)
        
        return {
            "imported": True,
            "project": submission,
            "team_members": len(submission["team"]),
            "ready_for_registration": True
        }


class MLHIntegration:
    """
    Major League Hacking (MLH) Integration
    
    Features:
    - Hackathon verification
    - Team member validation
    - Event-based IP protection
    """
    
    def __init__(self):
        self.events = {}
        
    def verify_hackathon(self, event_id: str) -> dict:
        """Verify hackathon event"""
        return {
            "event_id": event_id,
            "name": "HackMIT 2026",
            "verified": True,
            "participants": 1500,
            "start_date": "2026-02-15",
            "end_date": "2026-02-17"
        }
    
    def register_team(self, event_id: str, team_name: str, 
                     members: List[str]) -> dict:
        """Register team for event-based IP protection"""
        return {
            "team_id": hashlib.md5(team_name.encode()).hexdigest()[:8],
            "team_name": team_name,
            "event": event_id,
            "members": members,
            "registered_at": datetime.datetime.now().isoformat(),
            "ip_protection_active": True
        }


class IntegrationHub:
    """
    Unified integration hub for all external platforms
    """
    
    def __init__(self):
        self.github = GitHubIntegration()
        self.devpost = DevpostIntegration()
        self.mlh = MLHIntegration()
        
    def import_from_github(self, repo_url: str) -> dict:
        """Import project from GitHub for registration"""
        # Parse repo URL
        match = re.match(r'github\.com/([^/]+)/([^/]+)', repo_url)
        if not match:
            return {"error": "Invalid GitHub URL"}
        
        owner, repo = match.groups()
        
        # Analyze contributions
        contributions = self.github.analyze_contributions(repo)
        
        return {
            "source": "github",
            "repository": f"{owner}/{repo}",
            "contributions": contributions,
            "ready_for_registration": True
        }
    
    def import_from_devpost(self, project_url: str) -> dict:
        """Import project from Devpost"""
        return self.devpost.import_project(project_url)
    
    def get_supported_platforms(self) -> List[dict]:
        """List all supported integration platforms"""
        return [
            {
                "name": "GitHub",
                "type": "code_repository",
                "features": ["OAuth", "Commit Analysis", "Webhooks", "Auto-sync"]
            },
            {
                "name": "Devpost",
                "type": "hackathon_platform",
                "features": ["Project Import", "Team Sync", "Badge Display"]
            },
            {
                "name": "MLH",
                "type": "hackathon_league",
                "features": ["Event Verification", "Team Registration"]
            },
            {
                "name": "GitLab",
                "type": "code_repository",
                "features": ["Coming Soon"]
            },
            {
                "name": "Bitbucket",
                "type": "code_repository", 
                "features": ["Coming Soon"]
            }
        ]
