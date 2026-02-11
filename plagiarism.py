"""
Plagiarism Detection Module
Simulates originality checking against web content
In production: Integrate with Turnitin API, Copyleaks, or custom ML model
"""

import hashlib
import re
from typing import Optional


# Simulated database of known plagiarized content (for demo)
KNOWN_PLAGIARISM_HASHES = {
    hashlib.md5(b"hello world program").hexdigest(),
    hashlib.md5(b"standard sorting algorithm").hexdigest(),
    hashlib.md5(b"basic todo list app").hexdigest(),
}

# Common phrases that indicate copy-paste
COMMON_BOILERPLATE = [
    "lorem ipsum",
    "hello world",
    "click here to learn more",
    "copyright all rights reserved",
    "sample code from",
    "copied from stackoverflow",
    "source: github",
]


def check_originality(content: str, threshold: float = 0.7) -> dict:
    """
    Check content originality
    
    Returns:
        dict with score (0-1), status, and details
    """
    content_lower = content.lower()
    score = 1.0
    issues = []
    
    # Check 1: Known plagiarism patterns
    content_hash = hashlib.md5(content_lower.encode()).hexdigest()
    if content_hash in KNOWN_PLAGIARISM_HASHES:
        score -= 0.5
        issues.append("Content matches known plagiarized material")
    
    # Check 2: Boilerplate detection
    boilerplate_count = sum(1 for bp in COMMON_BOILERPLATE if bp in content_lower)
    if boilerplate_count > 0:
        score -= boilerplate_count * 0.05
        issues.append(f"Found {boilerplate_count} common boilerplate phrases")
    
    # Check 3: Content length (too short = suspicious)
    word_count = len(content.split())
    if word_count < 50:
        score -= 0.1
        issues.append("Content too short for reliable analysis")
    
    # Check 4: Unique vocabulary ratio
    words = re.findall(r'\b\w+\b', content_lower)
    unique_ratio = len(set(words)) / len(words) if words else 0
    if unique_ratio < 0.3:
        score -= 0.15
        issues.append("Low vocabulary diversity detected")
    
    # Check 5: Technical depth (more technical = more original)
    tech_indicators = [
        'algorithm', 'implementation', 'architecture', 'optimization',
        'neural', 'blockchain', 'api', 'database', 'encryption'
    ]
    tech_count = sum(1 for t in tech_indicators if t in content_lower)
    if tech_count > 3:
        score += 0.05  # Bonus for technical depth
    
    # Check 6: Code presence (original code is good)
    has_code = any(pattern in content for pattern in [
        'def ', 'function ', 'class ', '=> {', 'const ', 'import '
    ])
    if has_code:
        score += 0.05
    
    # Normalize score
    score = max(0.0, min(1.0, score))
    
    # Determine status
    if score >= 0.9:
        status = "✅ HIGHLY ORIGINAL"
    elif score >= threshold:
        status = "✅ ORIGINAL"
    elif score >= 0.5:
        status = "⚠️ NEEDS REVIEW"
    else:
        status = "❌ LIKELY PLAGIARIZED"
    
    return {
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold,
        "status": status,
        "issues": issues,
        "word_count": word_count,
        "unique_vocabulary_ratio": round(unique_ratio, 2)
    }


def deep_plagiarism_check(content: str, sources: Optional[list] = None) -> dict:
    """
    Extended plagiarism check against external sources
    
    In production:
    - Query Turnitin/Copyleaks API
    - Search GitHub for code matches
    - Check academic databases
    - Use embedding similarity against known content
    """
    basic_check = check_originality(content)
    
    # Simulate external API check
    external_score = 0.95  # Simulated external verification
    
    # Combine scores
    combined_score = (basic_check['score'] * 0.6) + (external_score * 0.4)
    
    return {
        **basic_check,
        "external_check": {
            "score": external_score,
            "sources_checked": ["GitHub", "StackOverflow", "Academic DB"],
            "matches_found": 0
        },
        "combined_score": combined_score
    }


# Production API integration example (commented out)
"""
import requests

class TurnitinChecker:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.turnitin.com/v1"
    
    def check(self, content: str) -> dict:
        response = requests.post(
            f"{self.base_url}/submissions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"content": content}
        )
        result = response.json()
        return {
            "score": 1 - (result['similarity_score'] / 100),
            "matches": result['matches']
        }


class CopyleaksChecker:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def check(self, content: str) -> dict:
        # Implementation for Copyleaks API
        pass
"""
