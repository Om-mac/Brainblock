# 🧠 BrainBlock

**Student IP & Project Timestamp System**

Protect your hackathon ideas and final year projects with AI-powered fingerprinting and blockchain timestamps.

## Quick Start

```bash
cd brainblock
python demo.py
```

## Features

| Feature | Description |
|---------|-------------|
| AI Fingerprinting | NLP analysis generates unique project signature |
| Plagiarism Check | Verify originality before registration |
| Blockchain Timestamp | Immutable Algorand transaction as proof |
| Co-Creator Vault | Fair ownership splits for group projects |
| Smart Contracts | Automated dispute resolution |

## Usage

### Single Project

```python
from brainblock import BrainBlock

bb = BrainBlock()
result = bb.submit_project(
    title="My Innovative Project",
    content="Description of my unique algorithm...",
    author="Your Name",
    wallet="YOUR_ALGORAND_WALLET_ADDRESS"
)

print(result['proof_url'])  # Share this to prove ownership
```

### Group Project

```python
from brainblock import BrainBlock, Contributor

bb = BrainBlock()
contributors = [
    Contributor(
        name="Alice",
        wallet_address="ALGO...",
        contribution="Core algorithm design...",
        contribution_type="algorithm"
    ),
    Contributor(
        name="Bob", 
        wallet_address="ALGO...",
        contribution="Frontend implementation...",
        contribution_type="implementation"
    )
]

result = bb.submit_group_project(
    title="Our Team Project",
    contributors=contributors
)

# AI suggests fair ownership split automatically
```

## Architecture

```
brainblock/
├── main.py          # Core BrainBlock system
├── fingerprint.py   # AI fingerprinting (NLP)
├── plagiarism.py    # Originality checking
├── blockchain.py    # Algorand simulator
└── demo.py          # Demo runner
```

## How It Works

1. **Upload** → Student submits project content
2. **Analyze** → AI extracts keywords & innovation score
3. **Verify** → Plagiarism check confirms originality  
4. **Register** → Hash embedded in Algorand transaction
5. **Prove** → Share blockchain explorer link as proof

## Production Deployment

Replace simulator with real Algorand SDK:

```python
from algosdk import account, transaction
from algosdk.v2client import algod

# Connect to Algorand
client = algod.AlgodClient(token, address)

# Create real transaction
txn = transaction.PaymentTxn(
    sender=wallet,
    sp=client.suggested_params(),
    receiver=wallet,
    amt=0,
    note=json.dumps(metadata).encode()
)
```

## License

MIT License - Open for educational use
