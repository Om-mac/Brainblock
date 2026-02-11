<p align="center">
  <img src="https://img.shields.io/badge/Hackathon-Project-blueviolet?style=for-the-badge" alt="Hackathon">
  <img src="https://img.shields.io/badge/Blockchain-Algorand-00D4AA?style=for-the-badge&logo=algorand" alt="Algorand">
  <img src="https://img.shields.io/badge/AI-Powered-FF6B6B?style=for-the-badge" alt="AI">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</p>

<h1 align="center">🧠 BrainBlock</h1>

<p align="center">
  <strong>Protecting Student Innovation with AI + Blockchain</strong>
</p>

<p align="center">
  <em>Your ideas deserve protection. BrainBlock creates immutable, timestamped proof of intellectual property ownership for hackathon projects and student innovations.</em>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-demo">Demo</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-api">API</a>
</p>

---

## 🎯 The Problem

> *"I thought of this first, but I can't prove it!"*

Students face real challenges protecting their innovations:
- 😰 Fear of ideas being stolen by peers or faculty
- 💸 No affordable way to prove "I created this first"
- 👥 Disputes over credit in group projects
- 📝 Lack of verifiable ownership records

## 💡 The Solution

**BrainBlock** combines AI-powered analysis with blockchain technology to create **unforgeable, timestamped proof** of intellectual property ownership.

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   📝 Upload Project  →  🤖 AI Analysis  →  ⛓️ Blockchain Record  │
│                                                                  │
│   Your code/idea       Fingerprint &        Immutable proof     │
│   goes in              originality check    forever on-chain    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Om-mac/Brainblock.git
cd Brainblock

# Run the interactive demo
python demo.py

# Or launch the visual showcase
python showcase.py

# Or use the CLI
python cli.py
```

---

## ✨ Features

### 🤖 AI-Powered Innovation Fingerprinting
- **Transformer embeddings** for semantic understanding
- **NLP analysis** extracts key innovations and algorithms
- **Novelty detection** scores your work's originality
- **Code language detection** for multi-language projects

### ⛓️ Algorand Blockchain Registration
- **Immutable timestamps** that can't be altered
- **Cryptographic hashing** (SHA-256) of your content
- **Public verification** via block explorer
- **Smart contracts** for group ownership

### 👥 Co-Creator Vault
- **AI-calculated fair splits** based on contribution analysis
- **Multi-signature smart contracts** for team projects
- **Transparent ownership** percentages on-chain
- **Dispute prevention** through clear attribution

### 🎨 NFT Minting
- **Algorand Standard Assets** (ASA) for IP ownership
- **ARC-69 compliant** metadata
- **Tradeable certificates** of ownership
- **Visual NFT generation** with unique designs

### ⚖️ Dispute Resolution
- **AI Fairness Engine** for impartial analysis
- **Evidence scoring** with weighted credibility
- **Timeline verification** against blockchain records
- **Automated recommendations** for resolution

### 📜 Proof Certificates
- **Beautiful HTML certificates** for sharing
- **QR codes** for instant verification
- **Social media share links** (Twitter, LinkedIn, WhatsApp)
- **Printable ASCII certificates**

---

## 🎮 Demo

### Interactive Showcase
```bash
python showcase.py
```
Walk through all features with beautiful animations and explanations.

### CLI Interface
```bash
python cli.py
```
Full-featured command-line interface with rich terminal UI.

### Basic Demo
```bash
python demo.py
```
Quick demonstration of core functionality.

---

## 💻 Usage

### Individual Project

```python
from main import BrainBlock

bb = BrainBlock()
result = bb.submit_project(
    title="Neural Network Optimizer",
    content="""
    A novel approach to neural network training using
    quantum-inspired optimization techniques...
    
    def quantum_optimize(model):
        circuit = build_variational_circuit()
        return hybrid_optimization(circuit, model)
    """,
    author="Alice Johnson",
    wallet="ALGO_WALLET_ADDRESS"
)

# Get your blockchain proof
print(f"Proof URL: {result['proof_url']}")
print(f"Transaction: {result['blockchain']['tx_id']}")
```

### Group Project

```python
from main import BrainBlock, Contributor

bb = BrainBlock()

contributors = [
    Contributor(
        name="Alice",
        wallet_address="ALGO_ALICE",
        contribution="Core algorithm design with novel consensus mechanism...",
        contribution_type="algorithm"
    ),
    Contributor(
        name="Bob",
        wallet_address="ALGO_BOB",
        contribution="React dashboard with real-time visualization...",
        contribution_type="implementation"
    )
]

result = bb.submit_group_project(
    title="Decentralized Voting System",
    contributors=contributors
)

# AI automatically calculates fair ownership split
for c in result['contributors']:
    print(f"{c['name']}: {c['ownership_percentage']}%")
```

### NFT Minting

```python
from nft_minting import NFTMinter

minter = NFTMinter()

nft = minter.mint_ip_nft(
    title="My Innovation",
    description="A breakthrough in distributed computing",
    creator_name="Alice",
    creator_wallet="ALGO_WALLET",
    content_hash="sha256_hash_of_content",
    project_type="algorithm"
)

print(f"NFT Asset ID: {nft.asset_id}")
```

---

## 🏗️ Architecture

```
brainblock/
├── main.py              # 🎯 Core BrainBlock system
├── ai_engine.py         # 🤖 Transformer embeddings & novelty detection
├── blockchain.py        # ⛓️ Algorand blockchain simulator
├── fingerprint.py       # 🔍 AI fingerprinting engine
├── plagiarism.py        # ✅ Originality checking
├── analytics.py         # 📊 Dashboard & metrics
├── aws_cloud.py         # ☁️ AWS infrastructure integration
├── integrations.py      # 🔌 GitHub, Devpost, MLH connectors
├── wallet.py            # 💰 Algorand wallet management
├── notifications.py     # 📧 Email, push, webhook notifications
│
├── cli.py              # 💻 Beautiful CLI interface
├── api.py              # 🌐 REST API (Flask)
├── showcase.py         # 🎬 Interactive feature demo
├── demo.py             # 🎮 Quick demo runner
│
├── nft_minting.py       # 🎨 NFT creation & marketplace
├── qr_certificate.py    # 📜 QR codes & certificates
├── dispute_resolution.py # ⚖️ AI dispute resolution
├── templates.py         # 📁 Project templates
│
└── requirements.txt     # 📦 Dependencies
```

---

## 🌐 API

BrainBlock provides a complete REST API:

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/submit` | Submit individual project |
| `POST` | `/api/v1/submit/group` | Submit group project |
| `GET` | `/api/v1/verify` | Verify ownership by tx_id |
| `POST` | `/api/v1/analyze` | Analyze content only |
| `GET` | `/api/v1/certificate` | Generate certificate |
| `GET` | `/api/v1/stats` | Platform statistics |

### Example Request

```bash
curl -X POST http://localhost:5000/api/v1/submit \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Innovative Algorithm",
    "content": "A novel approach to...",
    "author": "Alice Johnson",
    "wallet_address": "ALGO_WALLET_123"
  }'
```

### Start API Server

```python
from api import create_flask_app
app = create_flask_app()
app.run(debug=True, port=5000)
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **AI/ML** | Transformer embeddings, NLP, Novelty detection |
| **Blockchain** | Algorand, Smart Contracts, ASA NFTs |
| **Cloud** | AWS (S3, DynamoDB, Lambda, SQS, Cognito) |
| **Backend** | Python, Flask |
| **Integrations** | GitHub, Devpost, MLH |
| **Auth** | Web3/WalletConnect, OAuth |

---

## 📊 How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          BRAINBLOCK WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. UPLOAD          2. ANALYZE           3. VERIFY          4. REGISTER │
│  ┌─────────┐       ┌─────────┐         ┌─────────┐        ┌─────────┐  │
│  │  📝     │  ──►  │  🤖     │   ──►   │  🔍     │  ──►   │  ⛓️     │  │
│  │ Project │       │ AI/NLP  │         │ Check   │        │ Algorand│  │
│  │ Content │       │ Analysis│         │ Origin  │        │ Record  │  │
│  └─────────┘       └─────────┘         └─────────┘        └─────────┘  │
│                                                                   │     │
│                                                                   ▼     │
│  5. SHARE                                               ┌─────────┐     │
│  ┌─────────────────────────────────────────────────────│  📜     │     │
│  │  🔗 Proof URL  │  📱 QR Code  │  🎨 NFT  │  📄 Cert  │ PROOF!  │     │
│  └─────────────────────────────────────────────────────└─────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🎪 Project Templates

BrainBlock includes templates for common hackathon projects:

| Category | Templates |
|----------|-----------|
| 🤖 **AI/ML** | Chatbot, Image Classifier, Recommender |
| ⛓️ **Blockchain** | DeFi Protocol, NFT Marketplace, DAO |
| 📱 **Web/Mobile** | Social Platform, E-Commerce, Dashboard |
| 💰 **FinTech** | Payment App, Trading Bot, Lending |
| 🏥 **HealthTech** | Health Monitor, Telemedicine, Diagnosis |
| 🎮 **Gaming** | Multiplayer Game, Game Engine, VR/AR |
| 🔒 **Security** | Security Audit, Password Manager, 2FA |

---

## 🏆 Hackathon Ready

BrainBlock is designed to impress:

- ✨ **Stunning Demos** - Beautiful ASCII art and animations
- 🎯 **Real Problem** - IP protection is a genuine pain point
- 💪 **Technical Depth** - AI + Blockchain integration
- 👥 **Group Projects** - Smart contract ownership splitting
- 🔗 **Shareable Proofs** - QR codes and certificates
- 📊 **Analytics** - Real-time metrics dashboard

---

## 🚀 Production Deployment

For production, replace the simulator with real Algorand SDK:

```python
from algosdk import account, transaction
from algosdk.v2client import algod

# Connect to Algorand
client = algod.AlgodClient(token, address)

# Create and sign real transactions
# Deploy actual smart contracts
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

---

## 📄 License

MIT License - Feel free to use for your hackathon!

---

<p align="center">
  <strong>Made with 🧠 for hackers, by hackers</strong>
</p>

<p align="center">
  <a href="https://github.com/Om-mac/Brainblock">⭐ Star this repo</a> if you find it helpful!
</p>

---

<p align="center">
  <sub>Built for hackathons. Powered by AI. Secured by Algorand blockchain.</sub>
</p>
