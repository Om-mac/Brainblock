"""
Project Templates & Categories
Pre-built templates for common hackathon project types
"""

from typing import List, Optional
from dataclasses import dataclass, field
import datetime


@dataclass
class ProjectTemplate:
    """Template for project registration"""
    id: str
    name: str
    category: str
    description: str
    fields: List[dict]
    sample_content: str
    keywords: List[str] = field(default_factory=list)
    icon: str = "📁"


# =============================================================================
# PROJECT CATEGORIES
# =============================================================================

CATEGORIES = {
    "ai_ml": {
        "name": "AI & Machine Learning",
        "icon": "🤖",
        "description": "Artificial intelligence and machine learning projects",
        "keywords": ["neural network", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "model"]
    },
    "blockchain": {
        "name": "Blockchain & Web3",
        "icon": "⛓️",
        "description": "Blockchain, cryptocurrency, and decentralized applications",
        "keywords": ["smart contract", "defi", "nft", "dao", "consensus", "wallet", "token"]
    },
    "web_mobile": {
        "name": "Web & Mobile Apps",
        "icon": "📱",
        "description": "Web applications and mobile development",
        "keywords": ["react", "flutter", "api", "frontend", "backend", "responsive", "pwa"]
    },
    "iot_hardware": {
        "name": "IoT & Hardware",
        "icon": "🔌",
        "description": "Internet of Things and hardware projects",
        "keywords": ["arduino", "raspberry pi", "sensor", "embedded", "firmware", "microcontroller"]
    },
    "fintech": {
        "name": "FinTech",
        "icon": "💰",
        "description": "Financial technology solutions",
        "keywords": ["payment", "banking", "trading", "insurance", "lending", "investment"]
    },
    "healthtech": {
        "name": "HealthTech",
        "icon": "🏥",
        "description": "Healthcare and medical technology",
        "keywords": ["medical", "diagnosis", "wellness", "telemedicine", "patient", "health"]
    },
    "edtech": {
        "name": "EdTech",
        "icon": "📚",
        "description": "Education technology solutions",
        "keywords": ["learning", "course", "student", "teacher", "assessment", "education"]
    },
    "sustainability": {
        "name": "Sustainability & Climate",
        "icon": "🌱",
        "description": "Environmental and sustainability projects",
        "keywords": ["green", "carbon", "sustainable", "renewable", "environment", "climate"]
    },
    "gaming": {
        "name": "Gaming & Entertainment",
        "icon": "🎮",
        "description": "Games and entertainment applications",
        "keywords": ["game", "unity", "unreal", "player", "multiplayer", "vr", "ar"]
    },
    "security": {
        "name": "Cybersecurity",
        "icon": "🔒",
        "description": "Security and privacy solutions",
        "keywords": ["encryption", "authentication", "vulnerability", "secure", "privacy", "protection"]
    }
}


# =============================================================================
# PROJECT TEMPLATES
# =============================================================================

TEMPLATES = [
    # AI/ML Templates
    ProjectTemplate(
        id="ai_chatbot",
        name="AI Chatbot",
        category="ai_ml",
        description="Conversational AI assistant using NLP",
        icon="💬",
        fields=[
            {"name": "model_type", "label": "Model Type", "type": "select", 
             "options": ["GPT-based", "BERT", "Custom Transformer", "Rule-based"]},
            {"name": "use_case", "label": "Use Case", "type": "text"},
            {"name": "training_data", "label": "Training Data Source", "type": "text"},
            {"name": "languages", "label": "Supported Languages", "type": "multiselect",
             "options": ["English", "Spanish", "French", "German", "Chinese", "Hindi"]}
        ],
        sample_content="""
# AI Chatbot Project

## Overview
An intelligent conversational assistant powered by transformer-based NLP.

## Technical Approach
- Model: Fine-tuned GPT-2/GPT-3 variant
- Framework: PyTorch + Hugging Face Transformers
- Deployment: FastAPI + Docker

## Key Features
- Context-aware conversations
- Multi-turn dialogue support
- Intent classification
- Entity extraction
- Sentiment analysis

## Innovation
Our unique contribution is the hybrid retrieval-generation approach that 
improves factual accuracy while maintaining conversational flow.

## Code Sample
```python
class ChatBot:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    def generate_response(self, user_input, context=[]):
        inputs = self.tokenizer(user_input, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=150)
        return self.tokenizer.decode(outputs[0])
```
        """,
        keywords=["chatbot", "nlp", "conversational ai", "transformer", "gpt"]
    ),
    
    ProjectTemplate(
        id="image_classifier",
        name="Image Classification System",
        category="ai_ml",
        description="Deep learning image recognition",
        icon="🖼️",
        fields=[
            {"name": "architecture", "label": "Model Architecture", "type": "select",
             "options": ["ResNet", "EfficientNet", "Vision Transformer", "Custom CNN"]},
            {"name": "dataset", "label": "Training Dataset", "type": "text"},
            {"name": "classes", "label": "Number of Classes", "type": "number"},
            {"name": "accuracy", "label": "Target Accuracy", "type": "text"}
        ],
        sample_content="""
# Image Classification System

## Overview
A high-accuracy image classification system using deep learning.

## Architecture
- Base Model: EfficientNet-B4
- Custom classification head
- Data augmentation pipeline
- Transfer learning approach

## Performance
- Accuracy: 97.5% on validation set
- Inference time: <50ms per image
- Model size: 75MB

## Code Sample
```python
class ImageClassifier:
    def __init__(self):
        self.model = EfficientNet.from_pretrained('efficientnet-b4')
        self.transform = get_transforms()
    
    def predict(self, image_path):
        image = Image.open(image_path)
        tensor = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            output = self.model(tensor)
        return torch.argmax(output, dim=1)
```
        """,
        keywords=["image classification", "cnn", "deep learning", "computer vision"]
    ),
    
    # Blockchain Templates
    ProjectTemplate(
        id="defi_protocol",
        name="DeFi Protocol",
        category="blockchain",
        description="Decentralized finance application",
        icon="🏦",
        fields=[
            {"name": "blockchain", "label": "Blockchain", "type": "select",
             "options": ["Algorand", "Ethereum", "Solana", "Polygon"]},
            {"name": "protocol_type", "label": "Protocol Type", "type": "select",
             "options": ["Lending", "DEX", "Yield Farming", "Staking", "Insurance"]},
            {"name": "tvl_target", "label": "Target TVL", "type": "text"},
            {"name": "audit_status", "label": "Audit Status", "type": "select",
             "options": ["Not Audited", "In Progress", "Audited"]}
        ],
        sample_content="""
# DeFi Protocol

## Overview
A decentralized lending protocol on Algorand blockchain.

## Features
- Collateralized lending
- Variable interest rates based on utilization
- Liquidation mechanism
- Governance token

## Smart Contract
```python
from pyteal import *

def lending_protocol():
    # Deposit collateral
    deposit = Seq([
        Assert(Txn.amount() > Int(0)),
        App.localPut(Txn.sender(), Bytes("collateral"), 
                     App.localGet(Txn.sender(), Bytes("collateral")) + Txn.amount()),
        Approve()
    ])
    
    # Borrow against collateral
    borrow = Seq([
        Assert(calculate_borrow_limit() >= requested_amount),
        # Transfer borrowed amount
        Approve()
    ])
    
    return Cond(
        [Txn.application_args[0] == Bytes("deposit"), deposit],
        [Txn.application_args[0] == Bytes("borrow"), borrow]
    )
```
        """,
        keywords=["defi", "lending", "smart contract", "algorand", "tvl"]
    ),
    
    ProjectTemplate(
        id="nft_marketplace",
        name="NFT Marketplace",
        category="blockchain",
        description="Digital collectibles marketplace",
        icon="🎨",
        fields=[
            {"name": "blockchain", "label": "Blockchain", "type": "select",
             "options": ["Algorand", "Ethereum", "Solana", "Tezos"]},
            {"name": "nft_types", "label": "NFT Types", "type": "multiselect",
             "options": ["Art", "Music", "Gaming", "Collectibles", "Domain Names"]},
            {"name": "royalties", "label": "Creator Royalties", "type": "text"}
        ],
        sample_content="""
# NFT Marketplace

## Overview
A user-friendly NFT marketplace for digital art and collectibles.

## Features
- Create and mint NFTs
- List for fixed price or auction
- Creator royalties on secondary sales
- Collection management
- Verified creators

## Technical Stack
- Frontend: Next.js + TailwindCSS
- Backend: Node.js + PostgreSQL
- Blockchain: Algorand ASA (ARC-69)
- Storage: IPFS

## Smart Contract
```python
def create_nft(name, metadata_url, royalty_percentage):
    # ASA creation for NFT
    return App.globalPut(
        Bytes("nft_" + str(asset_id)),
        Concat(name, metadata_url, royalty)
    )
```
        """,
        keywords=["nft", "marketplace", "digital art", "collectibles"]
    ),
    
    # Web/Mobile Templates
    ProjectTemplate(
        id="social_platform",
        name="Social Platform",
        category="web_mobile",
        description="Social networking application",
        icon="👥",
        fields=[
            {"name": "platform", "label": "Platform", "type": "multiselect",
             "options": ["Web", "iOS", "Android"]},
            {"name": "features", "label": "Core Features", "type": "multiselect",
             "options": ["Posts", "Stories", "DMs", "Groups", "Live Video"]},
            {"name": "tech_stack", "label": "Tech Stack", "type": "text"}
        ],
        sample_content="""
# Social Platform

## Overview
A next-generation social platform focused on authentic connections.

## Features
- Real-time feed with algorithmic curation
- Stories and ephemeral content
- Direct messaging with E2E encryption
- Community groups and events
- Creator monetization tools

## Tech Stack
- Frontend: React Native (cross-platform)
- Backend: Node.js + GraphQL
- Database: PostgreSQL + Redis
- Real-time: WebSockets
- CDN: CloudFlare
        """,
        keywords=["social media", "platform", "react native", "real-time"]
    ),
    
    ProjectTemplate(
        id="ecommerce",
        name="E-Commerce Platform",
        category="web_mobile",
        description="Online shopping application",
        icon="🛒",
        fields=[
            {"name": "platform", "label": "Platform", "type": "select",
             "options": ["Web Only", "Web + Mobile", "Mobile Only"]},
            {"name": "payment_methods", "label": "Payment Methods", "type": "multiselect",
             "options": ["Credit Card", "PayPal", "Crypto", "Bank Transfer"]},
            {"name": "scale", "label": "Expected Scale", "type": "text"}
        ],
        sample_content="""
# E-Commerce Platform

## Overview
A modern e-commerce platform with personalized shopping experience.

## Features
- AI-powered product recommendations
- Real-time inventory management
- Multi-vendor support
- Integrated payment processing
- Order tracking and notifications

## Technical Innovation
- Machine learning for personalization
- Microservices architecture for scalability
- Headless CMS for content management
        """,
        keywords=["ecommerce", "shopping", "marketplace", "payments"]
    ),
    
    # FinTech Templates
    ProjectTemplate(
        id="payment_app",
        name="Payment Application",
        category="fintech",
        description="Digital payment solution",
        icon="💳",
        fields=[
            {"name": "payment_type", "label": "Payment Type", "type": "select",
             "options": ["P2P", "B2B", "B2C", "Cross-border"]},
            {"name": "currencies", "label": "Supported Currencies", "type": "text"},
            {"name": "compliance", "label": "Compliance", "type": "multiselect",
             "options": ["PCI DSS", "GDPR", "PSD2", "KYC/AML"]}
        ],
        sample_content="""
# Payment Application

## Overview
A seamless digital payment application for instant transfers.

## Features
- Instant P2P transfers
- Bill splitting
- QR code payments
- Multi-currency support
- Transaction history and analytics

## Security
- End-to-end encryption
- Biometric authentication
- Fraud detection AI
- PCI DSS compliant
        """,
        keywords=["payment", "fintech", "transfer", "mobile wallet"]
    ),
    
    # HealthTech Templates
    ProjectTemplate(
        id="health_monitor",
        name="Health Monitoring System",
        category="healthtech",
        description="Patient health tracking solution",
        icon="❤️",
        fields=[
            {"name": "metrics", "label": "Health Metrics", "type": "multiselect",
             "options": ["Heart Rate", "Blood Pressure", "SpO2", "Temperature", "Sleep"]},
            {"name": "integration", "label": "Device Integration", "type": "multiselect",
             "options": ["Apple Watch", "Fitbit", "Garmin", "Custom IoT"]},
            {"name": "compliance", "label": "Compliance", "type": "select",
             "options": ["HIPAA", "GDPR", "Both"]}
        ],
        sample_content="""
# Health Monitoring System

## Overview
Continuous health monitoring with AI-powered insights.

## Features
- Real-time vital signs tracking
- AI anomaly detection
- Doctor dashboard integration
- Emergency alerts
- Health trends and analytics

## Technical Approach
- Wearable device integration via BLE
- ML models for anomaly detection
- HIPAA-compliant cloud storage
- Real-time notification system
        """,
        keywords=["health", "monitoring", "wearable", "telemedicine", "ai"]
    ),
    
    # Gaming Templates
    ProjectTemplate(
        id="multiplayer_game",
        name="Multiplayer Game",
        category="gaming",
        description="Real-time multiplayer gaming experience",
        icon="🎮",
        fields=[
            {"name": "game_type", "label": "Game Type", "type": "select",
             "options": ["Battle Royale", "MMORPG", "Strategy", "Racing", "Puzzle"]},
            {"name": "platform", "label": "Platform", "type": "multiselect",
             "options": ["PC", "Console", "Mobile", "Web"]},
            {"name": "engine", "label": "Game Engine", "type": "select",
             "options": ["Unity", "Unreal", "Godot", "Custom"]}
        ],
        sample_content="""
# Multiplayer Game

## Overview
An innovative multiplayer gaming experience with unique mechanics.

## Features
- Real-time multiplayer (up to 100 players)
- Cross-platform play
- Skill-based matchmaking
- In-game economy
- Seasonal content updates

## Technical Architecture
- Game Engine: Unity with custom netcode
- Backend: Dedicated game servers
- Matchmaking: Custom ELO system
- Database: Redis for real-time, PostgreSQL for persistence
        """,
        keywords=["game", "multiplayer", "unity", "real-time"]
    ),
    
    # Security Templates
    ProjectTemplate(
        id="security_audit",
        name="Security Audit Tool",
        category="security",
        description="Automated security vulnerability scanner",
        icon="🔍",
        fields=[
            {"name": "scan_type", "label": "Scan Type", "type": "multiselect",
             "options": ["Web App", "API", "Smart Contract", "Network", "Mobile"]},
            {"name": "detection", "label": "Detection Methods", "type": "multiselect",
             "options": ["Static Analysis", "Dynamic Analysis", "Fuzzing", "AI-based"]},
            {"name": "output", "label": "Report Format", "type": "multiselect",
             "options": ["PDF", "JSON", "HTML", "SARIF"]}
        ],
        sample_content="""
# Security Audit Tool

## Overview
Automated security vulnerability scanner for modern applications.

## Features
- OWASP Top 10 detection
- Smart contract vulnerability scanning
- API security testing
- Detailed remediation guidance
- CI/CD integration

## Technical Approach
- Static analysis using AST parsing
- Dynamic testing with headless browser
- ML-based vulnerability classification
- Custom rule engine
        """,
        keywords=["security", "vulnerability", "scanner", "audit", "owasp"]
    )
]


class TemplateManager:
    """Manage project templates"""
    
    def __init__(self):
        self.templates = {t.id: t for t in TEMPLATES}
        self.categories = CATEGORIES
        
    def get_template(self, template_id: str) -> Optional[ProjectTemplate]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def get_templates_by_category(self, category: str) -> List[ProjectTemplate]:
        """Get all templates in a category"""
        return [t for t in TEMPLATES if t.category == category]
    
    def get_all_categories(self) -> dict:
        """Get all categories"""
        return self.categories
    
    def search_templates(self, query: str) -> List[ProjectTemplate]:
        """Search templates by keyword"""
        query = query.lower()
        results = []
        
        for template in TEMPLATES:
            if (query in template.name.lower() or 
                query in template.description.lower() or
                any(query in kw for kw in template.keywords)):
                results.append(template)
        
        return results
    
    def suggest_category(self, content: str) -> str:
        """Suggest category based on content analysis"""
        content_lower = content.lower()
        
        # Count keyword matches for each category
        scores = {}
        for cat_id, cat_info in self.categories.items():
            score = sum(1 for kw in cat_info['keywords'] if kw in content_lower)
            scores[cat_id] = score
        
        # Return category with highest score
        if scores:
            best_cat = max(scores, key=scores.get)
            if scores[best_cat] > 0:
                return best_cat
        
        return "web_mobile"  # Default category
    
    def generate_from_template(self, template_id: str, values: dict) -> dict:
        """Generate project content from template"""
        template = self.get_template(template_id)
        if not template:
            return {"error": "Template not found"}
        
        # Generate content with values
        generated = {
            "template": template_id,
            "category": template.category,
            "generated_at": datetime.datetime.now().isoformat(),
            "values": values,
            "content": template.sample_content,
            "suggested_keywords": template.keywords
        }
        
        return generated
    
    def print_template_catalog(self):
        """Print available templates"""
        print("\n" + "="*70)
        print("📁 BRAINBLOCK PROJECT TEMPLATE CATALOG")
        print("="*70)
        
        for cat_id, cat_info in self.categories.items():
            templates = self.get_templates_by_category(cat_id)
            if templates:
                print(f"\n{cat_info['icon']} {cat_info['name']}")
                print("-" * 50)
                for t in templates:
                    print(f"   {t.icon} {t.name}")
                    print(f"      ID: {t.id}")
                    print(f"      {t.description}")


def demo_templates():
    """Demo the template system"""
    print("\n" + "="*70)
    print("📁 PROJECT TEMPLATES DEMO")
    print("="*70)
    
    manager = TemplateManager()
    
    # Print catalog
    manager.print_template_catalog()
    
    # Search demo
    print("\n\n🔍 Search Results for 'blockchain':")
    print("-" * 50)
    results = manager.search_templates("blockchain")
    for t in results:
        print(f"   {t.icon} {t.name} - {t.description}")
    
    # Category suggestion
    print("\n\n🤖 Category Suggestion Demo:")
    print("-" * 50)
    sample_content = """
    A decentralized application that uses smart contracts for 
    tokenized asset trading with automated market making.
    """
    suggested = manager.suggest_category(sample_content)
    cat = manager.categories[suggested]
    print(f"   Content: \"{sample_content.strip()[:50]}...\"")
    print(f"   Suggested Category: {cat['icon']} {cat['name']}")
    
    print("\n" + "="*70)
    print("✅ TEMPLATE DEMO COMPLETE")
    print("="*70)


if __name__ == "__main__":
    demo_templates()
