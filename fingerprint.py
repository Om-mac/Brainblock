"""
AI Fingerprinting Module
Generates unique fingerprints for project submissions using NLP
"""

import hashlib
import re
from collections import Counter


# Technical keywords database (simplified for demo)
TECHNICAL_KEYWORDS = {
    'algorithm', 'machine learning', 'neural network', 'blockchain', 'api',
    'database', 'optimization', 'encryption', 'authentication', 'deep learning',
    'computer vision', 'natural language', 'distributed', 'scalable', 'real-time',
    'artificial intelligence', 'data structure', 'hash', 'cryptography', 'protocol',
    'smart contract', 'decentralized', 'consensus', 'validation', 'automation'
}

INNOVATION_INDICATORS = {
    'novel', 'unique', 'innovative', 'first', 'new approach', 'breakthrough',
    'improved', 'enhanced', 'original', 'proprietary', 'custom', 'hybrid',
    'state-of-the-art', 'cutting-edge', 'advanced', 'revolutionary'
}


def extract_keywords(text: str) -> list[str]:
    """Extract technical keywords from text"""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Find matching technical keywords
    found_keywords = []
    for keyword in TECHNICAL_KEYWORDS:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    # Also extract capitalized terms (likely technical terms)
    capitalized = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
    found_keywords.extend([w.lower() for w in capitalized if len(w) > 3])
    
    # Count word frequency for important terms
    word_freq = Counter(words)
    frequent_technical = [
        word for word, count in word_freq.most_common(20)
        if len(word) > 4 and count > 1
    ]
    found_keywords.extend(frequent_technical)
    
    return list(set(found_keywords))[:10]


def calculate_innovation_score(text: str) -> float:
    """Calculate an innovation score based on content analysis"""
    text_lower = text.lower()
    score = 0.5  # Base score
    
    # Check for innovation indicators
    indicator_count = sum(1 for ind in INNOVATION_INDICATORS if ind in text_lower)
    score += min(indicator_count * 0.05, 0.25)
    
    # Check for technical depth
    tech_count = sum(1 for kw in TECHNICAL_KEYWORDS if kw in text_lower)
    score += min(tech_count * 0.03, 0.15)
    
    # Check for code presence
    code_indicators = ['def ', 'function', 'class ', 'import ', 'const ', 'let ', 'var ']
    has_code = any(ind in text for ind in code_indicators)
    if has_code:
        score += 0.1
    
    # Normalize to 0-1 range
    return min(max(score, 0.0), 1.0)


def calculate_complexity(text: str) -> str:
    """Estimate project complexity"""
    word_count = len(text.split())
    tech_keywords = extract_keywords(text)
    
    if word_count > 500 and len(tech_keywords) > 7:
        return "HIGH"
    elif word_count > 200 and len(tech_keywords) > 4:
        return "MEDIUM"
    else:
        return "LOW"


def generate_fingerprint(content: str) -> dict:
    """
    Generate a unique fingerprint for the content
    Combines NLP analysis with cryptographic hashing
    """
    keywords = extract_keywords(content)
    innovation_score = calculate_innovation_score(content)
    complexity = calculate_complexity(content)
    
    # Create deterministic fingerprint components
    keyword_hash = hashlib.md5('|'.join(sorted(keywords)).encode()).hexdigest()[:8]
    content_signature = hashlib.sha256(content.encode()).hexdigest()[:12]
    
    fingerprint = {
        "keywords": keywords,
        "innovation_score": innovation_score,
        "complexity": complexity,
        "keyword_hash": keyword_hash,
        "content_signature": content_signature,
        "word_count": len(content.split()),
        "unique_id": f"BRB-{keyword_hash}-{content_signature[:8]}"
    }
    
    return fingerprint


def compare_fingerprints(fp1: dict, fp2: dict) -> float:
    """Compare two fingerprints and return similarity score"""
    # Compare keyword overlap
    kw1 = set(fp1.get('keywords', []))
    kw2 = set(fp2.get('keywords', []))
    
    if not kw1 or not kw2:
        return 0.0
    
    overlap = len(kw1 & kw2)
    total = len(kw1 | kw2)
    
    keyword_similarity = overlap / total if total > 0 else 0
    
    # Compare content signatures
    sig_match = fp1.get('content_signature') == fp2.get('content_signature')
    
    if sig_match:
        return 1.0  # Exact match
    
    return keyword_similarity
