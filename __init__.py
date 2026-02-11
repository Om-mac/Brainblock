"""
BrainBlock: Student IP & Project Timestamp System
Protects student intellectual property with AI + Blockchain
"""

from .main import BrainBlock, Submission, Contributor
from .fingerprint import generate_fingerprint, extract_keywords
from .plagiarism import check_originality
from .blockchain import AlgorandSimulator

__version__ = "1.0.0"
__all__ = [
    "BrainBlock",
    "Submission", 
    "Contributor",
    "generate_fingerprint",
    "extract_keywords",
    "check_originality",
    "AlgorandSimulator"
]
