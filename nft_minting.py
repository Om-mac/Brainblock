"""
NFT Minting Module
Mint IP ownership as Algorand Standard Assets (ASA) NFTs
"""

import hashlib
import datetime
import random
import string
import json
from typing import Optional, List
from dataclasses import dataclass, field, asdict


@dataclass
class NFTMetadata:
    """Metadata for IP NFT following ARC-69 standard"""
    name: str
    description: str
    creator: str
    created_at: str
    properties: dict = field(default_factory=dict)
    external_url: str = ""
    image: str = ""
    animation_url: str = ""
    
    def to_arc69(self) -> dict:
        """Convert to ARC-69 standard format"""
        return {
            "standard": "arc69",
            "description": self.description,
            "external_url": self.external_url,
            "mime_type": "application/json",
            "properties": {
                "creator": self.creator,
                "created_at": self.created_at,
                **self.properties
            }
        }


@dataclass
class IPNFT:
    """Intellectual Property NFT representation"""
    asset_id: str
    name: str
    unit_name: str
    creator_address: str
    metadata: NFTMetadata
    total_supply: int = 1  # NFT is unique
    decimals: int = 0
    default_frozen: bool = False
    clawback_address: Optional[str] = None
    freeze_address: Optional[str] = None
    manager_address: Optional[str] = None
    reserve_address: Optional[str] = None
    tx_id: str = ""
    block: int = 0
    created_at: str = ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)


class NFTGenerator:
    """
    Generate visual NFT representations
    Creates ASCII art and SVG visualizations for IP NFTs
    """
    
    # Color schemes for different project types
    COLOR_SCHEMES = {
        "algorithm": ["#667eea", "#764ba2"],    # Purple gradient
        "implementation": ["#11998e", "#38ef7d"], # Green gradient
        "design": ["#ee0979", "#ff6a00"],        # Orange-pink gradient
        "docs": ["#2193b0", "#6dd5ed"],          # Blue gradient
        "research": ["#834d9b", "#d04ed6"],      # Magenta gradient
        "default": ["#1a1a2e", "#4a4a6a"]        # Dark gradient
    }
    
    def generate_nft_image_svg(self, 
                               title: str, 
                               creator: str, 
                               tx_id: str,
                               project_type: str = "default") -> str:
        """Generate SVG image for NFT"""
        colors = self.COLOR_SCHEMES.get(project_type, self.COLOR_SCHEMES["default"])
        
        # Generate unique pattern based on tx_id
        pattern_seed = int(hashlib.md5(tx_id.encode()).hexdigest()[:8], 16)
        random.seed(pattern_seed)
        
        # Generate circuit-like pattern
        circuit_paths = self._generate_circuit_pattern(pattern_seed)
        
        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{colors[0]};stop-opacity:1" />
            <stop offset="100%" style="stop-color:{colors[1]};stop-opacity:1" />
        </linearGradient>
        <linearGradient id="textGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#ffffff;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#f0f0f0;stop-opacity:0.9" />
        </linearGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Background -->
    <rect width="400" height="400" fill="url(#bgGradient)"/>
    
    <!-- Circuit pattern -->
    <g stroke="rgba(255,255,255,0.1)" stroke-width="1" fill="none">
        {circuit_paths}
    </g>
    
    <!-- Brain icon -->
    <g transform="translate(200, 120)" filter="url(#glow)">
        <text font-size="80" text-anchor="middle" fill="white">🧠</text>
    </g>
    
    <!-- Title -->
    <text x="200" y="200" font-family="Arial, sans-serif" font-size="18" 
          font-weight="bold" fill="white" text-anchor="middle">
        {title[:30]}{'...' if len(title) > 30 else ''}
    </text>
    
    <!-- Creator -->
    <text x="200" y="230" font-family="Arial, sans-serif" font-size="12" 
          fill="rgba(255,255,255,0.8)" text-anchor="middle">
        by {creator}
    </text>
    
    <!-- BrainBlock badge -->
    <g transform="translate(200, 280)">
        <rect x="-80" y="-15" width="160" height="30" rx="15" 
              fill="rgba(255,255,255,0.2)"/>
        <text font-family="Arial, sans-serif" font-size="11" 
              fill="white" text-anchor="middle" y="4">
            🔗 BRAINBLOCK VERIFIED
        </text>
    </g>
    
    <!-- TX ID -->
    <text x="200" y="330" font-family="monospace" font-size="8" 
          fill="rgba(255,255,255,0.5)" text-anchor="middle">
        TX: {tx_id[:32]}...
    </text>
    
    <!-- Border -->
    <rect x="5" y="5" width="390" height="390" rx="20"
          fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
          
    <!-- Corner accents -->
    <circle cx="30" cy="30" r="5" fill="rgba(255,255,255,0.5)"/>
    <circle cx="370" cy="30" r="5" fill="rgba(255,255,255,0.5)"/>
    <circle cx="30" cy="370" r="5" fill="rgba(255,255,255,0.5)"/>
    <circle cx="370" cy="370" r="5" fill="rgba(255,255,255,0.5)"/>
</svg>"""
        return svg
    
    def _generate_circuit_pattern(self, seed: int) -> str:
        """Generate circuit-like decorative pattern"""
        paths = []
        random.seed(seed)
        
        for _ in range(15):
            x1 = random.randint(0, 400)
            y1 = random.randint(0, 400)
            x2 = x1 + random.randint(-100, 100)
            y2 = y1
            x3 = x2
            y3 = y2 + random.randint(-100, 100)
            paths.append(f'<path d="M{x1},{y1} L{x2},{y2} L{x3},{y3}"/>')
            
            # Add nodes
            if random.random() > 0.5:
                paths.append(f'<circle cx="{x2}" cy="{y2}" r="3"/>')
        
        return '\n        '.join(paths)
    
    def generate_ascii_nft(self, title: str, creator: str, asset_id: str) -> str:
        """Generate ASCII art representation of NFT"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      ████████████████████████████████████████████████        ║
║      ██                                            ██        ║
║      ██                   🧠                       ██        ║
║      ██                                            ██        ║
║      ██     ██████╗ ██████╗  █████╗ ██╗███╗   ██╗  ██        ║
║      ██     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║  ██        ║
║      ██     ██████╔╝██████╔╝███████║██║██╔██╗ ██║  ██        ║
║      ██     ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║  ██        ║
║      ██     ██████╔╝██║  ██║██║  ██║██║██║ ╚████║  ██        ║
║      ██     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝  ██        ║
║      ██                                            ██        ║
║      ██               BLOCK IP NFT                 ██        ║
║      ██                                            ██        ║
║      ██  {title[:38]:^38}  ██        ║
║      ██                                            ██        ║
║      ██  Creator: {creator[:28]:<28}  ██        ║
║      ██  Asset ID: {asset_id[:27]:<27}  ██        ║
║      ██                                            ██        ║
║      ██            ✓ BLOCKCHAIN VERIFIED           ██        ║
║      ██                                            ██        ║
║      ████████████████████████████████████████████████        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """


class NFTMinter:
    """
    NFT Minting System for IP Protection
    
    Uses Algorand Standard Assets (ASA) for NFT creation
    Follows ARC-3 and ARC-69 metadata standards
    """
    
    def __init__(self):
        self.minted_nfts = {}
        self.generator = NFTGenerator()
        self.current_block = 35_000_000 + random.randint(1, 100000)
        
    def _generate_asset_id(self) -> str:
        """Generate unique Algorand asset ID"""
        return str(random.randint(100000000, 999999999))
    
    def _generate_tx_id(self) -> str:
        """Generate transaction ID"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=52))
    
    def _generate_unit_name(self, title: str) -> str:
        """Generate 8-character unit name for ASA"""
        # Remove special chars and take first 8 chars
        clean = ''.join(c for c in title.upper() if c.isalnum())
        return f"BB{clean[:6]}"
    
    def mint_ip_nft(self,
                    title: str,
                    description: str,
                    creator_name: str,
                    creator_wallet: str,
                    content_hash: str,
                    project_type: str = "default",
                    ownership_percentage: float = 100.0,
                    additional_properties: dict = None) -> IPNFT:
        """
        Mint a new IP ownership NFT
        
        Args:
            title: Project title
            description: Project description
            creator_name: Creator's name
            creator_wallet: Creator's Algorand wallet address
            content_hash: Hash of the protected content
            project_type: Type of project for visual styling
            ownership_percentage: Percentage of ownership represented
            additional_properties: Additional metadata properties
        
        Returns:
            IPNFT object with minting details
        """
        print(f"\n{'='*60}")
        print(f"🎨 MINTING IP NFT: {title}")
        print(f"{'='*60}")
        
        asset_id = self._generate_asset_id()
        tx_id = self._generate_tx_id()
        self.current_block += 1
        
        # Create metadata
        properties = {
            "content_hash": content_hash,
            "project_type": project_type,
            "ownership_percentage": ownership_percentage,
            "standard": "BrainBlock IP v1.0",
            "protected_at": datetime.datetime.now().isoformat()
        }
        if additional_properties:
            properties.update(additional_properties)
        
        metadata = NFTMetadata(
            name=f"BrainBlock: {title}",
            description=description,
            creator=creator_name,
            created_at=datetime.datetime.now().isoformat(),
            properties=properties,
            external_url=f"https://brainblock.io/nft/{asset_id}",
            image=f"https://brainblock.io/nft/{asset_id}/image.svg"
        )
        
        # Create NFT
        nft = IPNFT(
            asset_id=asset_id,
            name=f"BrainBlock: {title}",
            unit_name=self._generate_unit_name(title),
            creator_address=creator_wallet,
            metadata=metadata,
            tx_id=tx_id,
            block=self.current_block,
            created_at=datetime.datetime.now().isoformat()
        )
        
        # Store NFT
        self.minted_nfts[asset_id] = nft
        
        # Display minting info
        print(f"\n✅ NFT Minted Successfully!")
        print(f"\n📋 NFT Details:")
        print(f"   Asset ID: {asset_id}")
        print(f"   Unit Name: {nft.unit_name}")
        print(f"   Name: {nft.name}")
        print(f"   Creator: {creator_name}")
        print(f"   Ownership: {ownership_percentage}%")
        print(f"\n⛓️  Blockchain:")
        print(f"   Transaction: {tx_id[:30]}...")
        print(f"   Block: {self.current_block}")
        print(f"   Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
        
        return nft
    
    def mint_group_nfts(self,
                        title: str,
                        description: str,
                        content_hash: str,
                        contributors: List[dict]) -> List[IPNFT]:
        """
        Mint NFTs for group project with fractional ownership
        
        Each contributor receives an NFT representing their ownership percentage
        """
        print(f"\n{'='*60}")
        print(f"🎨 MINTING GROUP IP NFTs: {title}")
        print(f"👥 Contributors: {len(contributors)}")
        print(f"{'='*60}")
        
        nfts = []
        
        for i, contrib in enumerate(contributors):
            print(f"\n[{i+1}/{len(contributors)}] Minting for {contrib['name']}...")
            
            nft = self.mint_ip_nft(
                title=f"{title} - {contrib['name']}'s Share",
                description=f"{description}\n\nThis NFT represents {contrib['ownership_percentage']}% ownership by {contrib['name']}.",
                creator_name=contrib['name'],
                creator_wallet=contrib['wallet_address'],
                content_hash=content_hash,
                project_type=contrib.get('contribution_type', 'implementation'),
                ownership_percentage=contrib['ownership_percentage'],
                additional_properties={
                    "group_project": title,
                    "total_contributors": len(contributors),
                    "contribution_type": contrib.get('contribution_type', 'general')
                }
            )
            nfts.append(nft)
        
        print(f"\n{'='*60}")
        print(f"✅ {len(nfts)} NFTs Minted for Group Project!")
        print(f"{'='*60}")
        
        return nfts
    
    def get_nft(self, asset_id: str) -> Optional[IPNFT]:
        """Retrieve NFT by asset ID"""
        return self.minted_nfts.get(asset_id)
    
    def get_nfts_by_wallet(self, wallet_address: str) -> List[IPNFT]:
        """Get all NFTs owned by a wallet"""
        return [
            nft for nft in self.minted_nfts.values()
            if nft.creator_address == wallet_address
        ]
    
    def get_nft_image(self, asset_id: str) -> str:
        """Get SVG image for NFT"""
        nft = self.get_nft(asset_id)
        if not nft:
            return None
        
        return self.generator.generate_nft_image_svg(
            title=nft.name.replace("BrainBlock: ", ""),
            creator=nft.metadata.creator,
            tx_id=nft.tx_id,
            project_type=nft.metadata.properties.get('project_type', 'default')
        )
    
    def get_nft_ascii_art(self, asset_id: str) -> str:
        """Get ASCII art for NFT"""
        nft = self.get_nft(asset_id)
        if not nft:
            return None
        
        return self.generator.generate_ascii_nft(
            title=nft.name.replace("BrainBlock: ", ""),
            creator=nft.metadata.creator,
            asset_id=asset_id
        )


class NFTMarketplace:
    """
    Simple NFT marketplace for IP trading
    (Demonstration purposes)
    """
    
    def __init__(self, minter: NFTMinter):
        self.minter = minter
        self.listings = {}
        self.sales_history = []
        
    def list_for_sale(self, asset_id: str, price_algo: float, seller_wallet: str) -> dict:
        """List an NFT for sale"""
        nft = self.minter.get_nft(asset_id)
        if not nft:
            return {"error": "NFT not found"}
        
        if nft.creator_address != seller_wallet:
            return {"error": "Only owner can list this NFT"}
        
        listing = {
            "asset_id": asset_id,
            "nft_name": nft.name,
            "price_algo": price_algo,
            "seller": seller_wallet,
            "listed_at": datetime.datetime.now().isoformat(),
            "status": "active"
        }
        
        self.listings[asset_id] = listing
        
        print(f"\n💰 NFT Listed for Sale!")
        print(f"   Name: {nft.name}")
        print(f"   Price: {price_algo} ALGO")
        
        return listing
    
    def get_listings(self) -> List[dict]:
        """Get all active listings"""
        return [l for l in self.listings.values() if l['status'] == 'active']
    
    def purchase(self, asset_id: str, buyer_wallet: str) -> dict:
        """Purchase an NFT (simulated)"""
        if asset_id not in self.listings:
            return {"error": "NFT not listed for sale"}
        
        listing = self.listings[asset_id]
        if listing['status'] != 'active':
            return {"error": "Listing is not active"}
        
        # Simulate purchase
        sale = {
            "asset_id": asset_id,
            "seller": listing['seller'],
            "buyer": buyer_wallet,
            "price_algo": listing['price_algo'],
            "sold_at": datetime.datetime.now().isoformat(),
            "tx_id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=52))
        }
        
        listing['status'] = 'sold'
        self.sales_history.append(sale)
        
        print(f"\n🎉 NFT Sold!")
        print(f"   Buyer: {buyer_wallet[:20]}...")
        print(f"   Price: {listing['price_algo']} ALGO")
        
        return sale


def demo_nft_minting():
    """Demo the NFT minting system"""
    print("\n" + "="*70)
    print("🎨 NFT MINTING SYSTEM DEMO")
    print("="*70)
    
    minter = NFTMinter()
    
    # Mint individual NFT
    print("\n📌 DEMO 1: Individual IP NFT")
    print("-" * 50)
    
    content_hash = hashlib.sha256(b"My innovative algorithm code...").hexdigest()
    
    nft = minter.mint_ip_nft(
        title="Neural Network Optimization Algorithm",
        description="A novel approach to neural network training that reduces computation by 40%",
        creator_name="Alice Johnson",
        creator_wallet="ALGO_ALICE_12345678901234567890123456789012345678901234",
        content_hash=content_hash,
        project_type="algorithm"
    )
    
    # Show ASCII art
    print("\n🖼️  NFT Visual Representation:")
    print(minter.get_nft_ascii_art(nft.asset_id))
    
    # Mint group NFTs
    print("\n📌 DEMO 2: Group Project NFTs")
    print("-" * 50)
    
    contributors = [
        {
            "name": "Bob Smith",
            "wallet_address": "ALGO_BOB_123456789",
            "ownership_percentage": 45,
            "contribution_type": "algorithm"
        },
        {
            "name": "Carol White",
            "wallet_address": "ALGO_CAROL_987654321",
            "ownership_percentage": 35,
            "contribution_type": "implementation"
        },
        {
            "name": "David Lee",
            "wallet_address": "ALGO_DAVID_456789123",
            "ownership_percentage": 20,
            "contribution_type": "design"
        }
    ]
    
    group_nfts = minter.mint_group_nfts(
        title="Decentralized Voting System",
        description="A blockchain-based voting system with zero-knowledge proofs",
        content_hash=hashlib.sha256(b"Group project code...").hexdigest(),
        contributors=contributors
    )
    
    # Marketplace demo
    print("\n📌 DEMO 3: NFT Marketplace")
    print("-" * 50)
    
    marketplace = NFTMarketplace(minter)
    
    # List NFT for sale
    listing = marketplace.list_for_sale(
        asset_id=nft.asset_id,
        price_algo=100.0,
        seller_wallet=nft.creator_address
    )
    
    # Show listings
    print("\n📊 Active Listings:")
    for l in marketplace.get_listings():
        print(f"   • {l['nft_name']} - {l['price_algo']} ALGO")
    
    # Purchase
    marketplace.purchase(
        asset_id=nft.asset_id,
        buyer_wallet="ALGO_BUYER_NEW_OWNER_ADDRESS"
    )
    
    print("\n" + "="*70)
    print("✅ NFT MINTING DEMO COMPLETE")
    print("="*70)


if __name__ == "__main__":
    demo_nft_minting()
