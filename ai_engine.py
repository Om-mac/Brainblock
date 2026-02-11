"""
Advanced AI Module
Deep learning models for content analysis, embedding generation, and novelty detection
"""

import hashlib
import math
import re
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class EmbeddingResult:
    """Result from embedding generation"""
    vector: List[float]
    dimensions: int
    model: str
    tokens: int


@dataclass
class NoveltyResult:
    """Result from novelty detection"""
    score: float
    confidence: float
    similar_items: List[dict]
    is_novel: bool


class TransformerEmbeddings:
    """
    Transformer-based Text Embeddings
    
    Production: Use sentence-transformers or OpenAI embeddings API
    Models:
    - all-MiniLM-L6-v2 (fast, 384 dims)
    - all-mpnet-base-v2 (balanced, 768 dims)
    - text-embedding-ada-002 (OpenAI, 1536 dims)
    """
    
    MODEL_DIMS = {
        "minilm": 384,
        "mpnet": 768,
        "ada-002": 1536,
        "custom": 512
    }
    
    def __init__(self, model: str = "mpnet"):
        self.model = model
        self.dims = self.MODEL_DIMS.get(model, 768)
        
    def encode(self, text: str) -> EmbeddingResult:
        """Generate embedding vector for text"""
        # Simulated embedding (deterministic based on content)
        tokens = text.split()
        
        # Create pseudo-embedding based on text hash
        seed = int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)
        vector = []
        for i in range(self.dims):
            # Deterministic pseudo-random values
            val = math.sin(seed * (i + 1)) * 0.5
            vector.append(round(val, 6))
        
        return EmbeddingResult(
            vector=vector,
            dimensions=self.dims,
            model=self.model,
            tokens=len(tokens)
        )
    
    def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
            
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)


class NoveltyDetector:
    """
    AI Novelty Detection System
    Determines how original/innovative a submission is
    """
    
    def __init__(self):
        self.embeddings = TransformerEmbeddings()
        self._known_embeddings = []  # Vector database (simulated)
        
    def detect_novelty(self, content: str) -> NoveltyResult:
        """Analyze content for novelty/originality"""
        
        # Generate embedding
        embedding = self.embeddings.encode(content)
        
        # Compare against known embeddings
        max_similarity = 0.0
        similar_items = []
        
        for known in self._known_embeddings:
            sim = self.embeddings.similarity(embedding.vector, known['vector'])
            if sim > max_similarity:
                max_similarity = sim
            if sim > 0.7:
                similar_items.append({
                    "id": known['id'],
                    "similarity": round(sim, 3),
                    "title": known.get('title', 'Unknown')
                })
        
        # Novelty is inverse of max similarity
        novelty_score = 1.0 - max_similarity
        
        # Apply content-based bonuses
        novelty_score = self._apply_content_bonuses(content, novelty_score)
        
        return NoveltyResult(
            score=round(novelty_score, 3),
            confidence=0.85,
            similar_items=similar_items[:5],
            is_novel=novelty_score > 0.6
        )
    
    def _apply_content_bonuses(self, content: str, base_score: float) -> float:
        """Apply bonuses based on content analysis"""
        score = base_score
        content_lower = content.lower()
        
        # Technical depth bonus
        tech_terms = ['algorithm', 'neural', 'blockchain', 'quantum', 'distributed',
                     'cryptographic', 'consensus', 'transformer', 'embedding']
        tech_count = sum(1 for t in tech_terms if t in content_lower)
        score += min(tech_count * 0.02, 0.15)
        
        # Code presence bonus
        if any(p in content for p in ['def ', 'function', 'class ', '=> {']):
            score += 0.05
        
        # Novel keyword bonus
        novel_terms = ['novel', 'unique', 'first', 'innovative', 'breakthrough']
        if any(n in content_lower for n in novel_terms):
            score += 0.03
        
        return min(score, 1.0)
    
    def add_to_index(self, content: str, metadata: dict) -> None:
        """Add content to the novelty index"""
        embedding = self.embeddings.encode(content)
        self._known_embeddings.append({
            "id": metadata.get('id', hashlib.md5(content.encode()).hexdigest()[:8]),
            "vector": embedding.vector,
            "title": metadata.get('title', ''),
            "timestamp": metadata.get('timestamp', '')
        })


class NLPProcessor:
    """
    Natural Language Processing for Innovation Extraction
    """
    
    # Innovation patterns to detect
    INNOVATION_PATTERNS = [
        r'(?:novel|new|unique|innovative)\s+(?:approach|method|algorithm|technique)',
        r'(?:first|pioneering)\s+(?:implementation|solution|system)',
        r'(?:improved|enhanced|optimized)\s+(?:performance|accuracy|efficiency)',
        r'(?:breakthrough|revolutionary|cutting-edge)\s+(?:technology|design|architecture)'
    ]
    
    # Technical entity patterns
    TECH_ENTITY_PATTERNS = {
        'algorithm': r'\b(?:algorithm|heuristic|optimizer)\b',
        'model': r'\b(?:model|network|classifier|transformer)\b',
        'framework': r'\b(?:framework|library|SDK|API)\b',
        'database': r'\b(?:database|datastore|cache|index)\b',
        'protocol': r'\b(?:protocol|standard|specification)\b'
    }
    
    def extract_innovations(self, text: str) -> List[dict]:
        """Extract innovation claims from text"""
        innovations = []
        
        for pattern in self.INNOVATION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                innovations.append({
                    "text": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "type": "innovation_claim"
                })
        
        return innovations
    
    def extract_entities(self, text: str) -> dict:
        """Extract technical entities from text"""
        entities = {}
        
        for entity_type, pattern in self.TECH_ENTITY_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                entities[entity_type] = list(set(matches))
        
        return entities
    
    def summarize(self, text: str, max_sentences: int = 3) -> str:
        """Generate a concise summary of the text"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Score sentences by importance (simplified)
        scored = []
        for sentence in sentences:
            score = 0
            # Favor sentences with technical terms
            if any(t in sentence.lower() for t in ['algorithm', 'model', 'system', 'approach']):
                score += 2
            # Favor sentences with numbers/metrics
            if re.search(r'\d+%|\d+\.\d+', sentence):
                score += 1
            # Favor shorter sentences
            if len(sentence.split()) < 25:
                score += 1
            scored.append((sentence, score))
        
        # Sort by score and take top sentences
        scored.sort(key=lambda x: x[1], reverse=True)
        summary_sentences = [s[0] for s in scored[:max_sentences]]
        
        return '. '.join(summary_sentences) + '.' if summary_sentences else text[:200]


class CodeAnalyzer:
    """
    Code-specific AI analysis
    """
    
    LANGUAGE_PATTERNS = {
        'python': [r'\bdef\s+\w+\s*\(', r'\bclass\s+\w+', r'import\s+\w+'],
        'javascript': [r'\bfunction\s+\w+', r'const\s+\w+\s*=', r'=>\s*{'],
        'java': [r'\bpublic\s+class', r'\bprivate\s+\w+', r'@Override'],
        'rust': [r'\bfn\s+\w+', r'\blet\s+mut', r'impl\s+\w+'],
        'go': [r'\bfunc\s+\w+', r'package\s+\w+', r':=']
    }
    
    def detect_language(self, code: str) -> str:
        """Detect programming language"""
        scores = {}
        
        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            score = sum(1 for p in patterns if re.search(p, code))
            scores[lang] = score
        
        if not scores or max(scores.values()) == 0:
            return "unknown"
        
        return max(scores, key=scores.get)
    
    def analyze_complexity(self, code: str) -> dict:
        """Analyze code complexity metrics"""
        lines = code.split('\n')
        
        return {
            "total_lines": len(lines),
            "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            "functions": len(re.findall(r'\bdef\s+\w+|\bfunction\s+\w+|\bfn\s+\w+', code)),
            "classes": len(re.findall(r'\bclass\s+\w+', code)),
            "imports": len(re.findall(r'\bimport\s+|\bfrom\s+\w+\s+import', code)),
            "comments": len([l for l in lines if l.strip().startswith('#') or l.strip().startswith('//')]),
            "complexity_score": self._calculate_complexity_score(code)
        }
    
    def _calculate_complexity_score(self, code: str) -> str:
        """Calculate overall complexity score"""
        metrics = {
            "conditionals": len(re.findall(r'\bif\b|\belse\b|\belif\b|\bswitch\b', code)),
            "loops": len(re.findall(r'\bfor\b|\bwhile\b|\bloop\b', code)),
            "functions": len(re.findall(r'\bdef\b|\bfunction\b|\bfn\b', code))
        }
        
        total = sum(metrics.values())
        
        if total > 20:
            return "HIGH"
        elif total > 10:
            return "MEDIUM"
        else:
            return "LOW"


class AIEngine:
    """
    Unified AI Engine combining all AI capabilities
    """
    
    def __init__(self):
        self.embeddings = TransformerEmbeddings()
        self.novelty = NoveltyDetector()
        self.nlp = NLPProcessor()
        self.code = CodeAnalyzer()
        
    def full_analysis(self, content: str) -> dict:
        """Perform comprehensive AI analysis on content"""
        
        # Generate embedding
        embedding = self.embeddings.encode(content)
        
        # Novelty detection
        novelty = self.novelty.detect_novelty(content)
        
        # NLP processing
        innovations = self.nlp.extract_innovations(content)
        entities = self.nlp.extract_entities(content)
        summary = self.nlp.summarize(content)
        
        # Check for code
        code_analysis = None
        if any(p in content for p in ['def ', 'function ', 'class ']):
            language = self.code.detect_language(content)
            code_analysis = {
                "language": language,
                "metrics": self.code.analyze_complexity(content)
            }
        
        return {
            "embedding": {
                "model": embedding.model,
                "dimensions": embedding.dimensions,
                "tokens": embedding.tokens
            },
            "novelty": {
                "score": novelty.score,
                "is_novel": novelty.is_novel,
                "confidence": novelty.confidence
            },
            "nlp": {
                "innovations_found": len(innovations),
                "innovations": innovations[:3],
                "entities": entities,
                "summary": summary
            },
            "code": code_analysis,
            "overall_innovation_score": round(
                (novelty.score * 0.6) + (len(innovations) * 0.1) + 
                (0.3 if code_analysis else 0), 2
            )
        }
