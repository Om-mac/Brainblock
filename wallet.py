"""
Wallet & Web3 Module
Algorand wallet management and Web3 authentication
"""

import hashlib
import secrets
import datetime
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Wallet:
    """Algorand wallet representation"""
    address: str
    public_key: str
    created_at: str
    balance: float = 0.0
    is_connected: bool = False


@dataclass
class Transaction:
    """Algorand transaction"""
    tx_id: str
    sender: str
    receiver: str
    amount: float
    fee: float
    note: str
    confirmed: bool
    block: int


class AlgorandWallet:
    """
    Algorand Wallet Management
    
    Supports:
    - Pera Wallet (mobile)
    - MyAlgo Wallet (web)
    - AlgoSigner (browser extension)
    - WalletConnect
    """
    
    SUPPORTED_WALLETS = [
        {
            "name": "Pera Wallet",
            "type": "mobile",
            "connect_method": "walletconnect",
            "icon": "pera-icon.svg"
        },
        {
            "name": "MyAlgo",
            "type": "web",
            "connect_method": "popup",
            "icon": "myalgo-icon.svg"
        },
        {
            "name": "AlgoSigner",
            "type": "extension",
            "connect_method": "injection",
            "icon": "algosigner-icon.svg"
        },
        {
            "name": "Defly",
            "type": "mobile",
            "connect_method": "walletconnect",
            "icon": "defly-icon.svg"
        }
    ]
    
    def __init__(self):
        self._wallets = {}
        self._connected_wallet = None
        
    def generate_wallet(self) -> Wallet:
        """
        Generate a new Algorand wallet
        
        Production: Use algosdk.account.generate_account()
        """
        # Generate deterministic test address
        private_key = secrets.token_hex(32)
        public_key = hashlib.sha256(private_key.encode()).hexdigest()
        
        # Algorand addresses are 58 characters
        address = "ALGO" + public_key[:54].upper()
        
        wallet = Wallet(
            address=address,
            public_key=public_key,
            created_at=datetime.datetime.now().isoformat()
        )
        
        self._wallets[address] = wallet
        return wallet
    
    def connect_pera(self) -> dict:
        """
        Connect Pera Wallet via WalletConnect
        
        Production flow:
        1. Generate WalletConnect URI
        2. Display QR code
        3. User scans with Pera app
        4. Receive account address
        """
        return {
            "method": "walletconnect",
            "uri": f"wc:{secrets.token_hex(16)}@2?relay-protocol=irn&symKey={secrets.token_hex(32)}",
            "status": "awaiting_connection",
            "qr_data": "data:image/png;base64,..."
        }
    
    def connect_myalgo(self) -> dict:
        """Connect MyAlgo Wallet via popup"""
        return {
            "method": "popup",
            "popup_url": "https://wallet.myalgo.com/access",
            "status": "awaiting_approval"
        }
    
    def connect_algosigner(self) -> dict:
        """Connect AlgoSigner browser extension"""
        return {
            "method": "injection",
            "extension_id": "algosigner",
            "status": "checking_extension"
        }
    
    def on_wallet_connected(self, address: str, wallet_type: str) -> dict:
        """Handle successful wallet connection"""
        wallet = Wallet(
            address=address,
            public_key=hashlib.sha256(address.encode()).hexdigest(),
            created_at=datetime.datetime.now().isoformat(),
            is_connected=True
        )
        
        self._wallets[address] = wallet
        self._connected_wallet = address
        
        return {
            "connected": True,
            "address": address,
            "wallet_type": wallet_type,
            "message": f"Successfully connected {wallet_type}"
        }
    
    def get_balance(self, address: str) -> dict:
        """Get wallet balance"""
        # Simulated balance check
        return {
            "address": address,
            "algo_balance": 10.5,
            "assets": [
                {"asset_id": 123456, "name": "USDC", "amount": 100.0},
                {"asset_id": 789012, "name": "BrainBlock Token", "amount": 500}
            ]
        }
    
    def sign_message(self, message: str, address: Optional[str] = None) -> dict:
        """
        Request wallet to sign a message
        Used for proving ownership
        """
        addr = address or self._connected_wallet
        if not addr:
            return {"error": "No wallet connected"}
        
        # Simulated signature
        signature = hashlib.sha512(f"{message}:{addr}".encode()).hexdigest()
        
        return {
            "address": addr,
            "message": message,
            "signature": signature,
            "algorithm": "ed25519"
        }
    
    def sign_transaction(self, tx_data: dict) -> dict:
        """
        Request wallet to sign a transaction
        """
        return {
            "status": "pending_signature",
            "tx_id": hashlib.sha256(str(tx_data).encode()).hexdigest()[:52],
            "requires_approval": True
        }


class WalletConnect:
    """
    WalletConnect v2 Protocol Implementation
    For connecting mobile wallets
    """
    
    def __init__(self, project_id: str = "brainblock"):
        self.project_id = project_id
        self._sessions = {}
        
    def create_session(self) -> dict:
        """Create new WalletConnect session"""
        session_id = secrets.token_hex(16)
        
        session = {
            "id": session_id,
            "topic": secrets.token_hex(32),
            "relay_protocol": "irn",
            "sym_key": secrets.token_hex(32),
            "created_at": datetime.datetime.now().isoformat(),
            "status": "pending"
        }
        
        self._sessions[session_id] = session
        
        # Generate connection URI
        uri = f"wc:{session['topic']}@2?relay-protocol={session['relay_protocol']}&symKey={session['sym_key']}"
        
        return {
            "session_id": session_id,
            "uri": uri,
            "expires_in": 300  # 5 minutes
        }
    
    def await_connection(self, session_id: str) -> dict:
        """Wait for wallet to connect"""
        if session_id not in self._sessions:
            return {"error": "Session not found"}
        
        # Simulated connection
        return {
            "connected": True,
            "chain": "algorand:testnet",
            "accounts": ["ALGO" + secrets.token_hex(27).upper()]
        }


class Web3Auth:
    """
    Web3 Authentication
    Sign-in with Algorand wallet (SIWA)
    """
    
    def __init__(self):
        self._challenges = {}
        
    def generate_challenge(self, address: str) -> dict:
        """Generate authentication challenge"""
        nonce = secrets.token_hex(16)
        timestamp = datetime.datetime.now().isoformat()
        
        message = f"""BrainBlock Authentication

Address: {address}
Nonce: {nonce}
Timestamp: {timestamp}

Sign this message to prove you own this wallet."""
        
        self._challenges[address] = {
            "nonce": nonce,
            "message": message,
            "timestamp": timestamp,
            "expires": 300
        }
        
        return {
            "address": address,
            "message": message,
            "nonce": nonce
        }
    
    def verify_signature(self, address: str, signature: str) -> dict:
        """Verify signed authentication challenge"""
        if address not in self._challenges:
            return {"verified": False, "error": "No challenge found"}
        
        # In production: Verify signature cryptographically
        # For demo: Accept any signature
        
        # Generate session token
        session_token = secrets.token_urlsafe(32)
        
        return {
            "verified": True,
            "address": address,
            "session_token": session_token,
            "expires_in": 86400  # 24 hours
        }
    
    def create_session(self, address: str) -> dict:
        """Create authenticated session"""
        return {
            "address": address,
            "session_id": secrets.token_hex(16),
            "created_at": datetime.datetime.now().isoformat(),
            "permissions": ["submit", "verify", "group"]
        }


class WalletHub:
    """
    Unified wallet management hub
    """
    
    def __init__(self):
        self.algorand = AlgorandWallet()
        self.walletconnect = WalletConnect()
        self.auth = Web3Auth()
        self._current_wallet = None
        
    def connect(self, wallet_type: str) -> dict:
        """Connect wallet by type"""
        if wallet_type == "pera":
            return self.algorand.connect_pera()
        elif wallet_type == "myalgo":
            return self.algorand.connect_myalgo()
        elif wallet_type == "algosigner":
            return self.algorand.connect_algosigner()
        else:
            return {"error": f"Unknown wallet type: {wallet_type}"}
    
    def get_supported_wallets(self) -> List[dict]:
        """Get list of supported wallets"""
        return AlgorandWallet.SUPPORTED_WALLETS
    
    def sign_in(self, address: str) -> dict:
        """Initiate sign-in with wallet"""
        return self.auth.generate_challenge(address)
    
    def complete_sign_in(self, address: str, signature: str) -> dict:
        """Complete sign-in process"""
        result = self.auth.verify_signature(address, signature)
        if result["verified"]:
            self._current_wallet = address
        return result
