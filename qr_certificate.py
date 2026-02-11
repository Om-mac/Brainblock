"""
QR Code & Certificate Generator
Generate shareable proofs and ownership certificates
"""

import base64
import hashlib
import datetime
from typing import Optional


class QRCodeGenerator:
    """
    QR Code Generator for Proof Sharing
    
    Production: Use qrcode library
    pip install qrcode[pil]
    """
    
    def __init__(self):
        self.base_url = "https://testnet.algoexplorer.io/tx"
        
    def generate_verification_url(self, tx_id: str) -> str:
        """Generate verification URL for a transaction"""
        return f"{self.base_url}/{tx_id}"
    
    def generate_qr_data(self, tx_id: str, title: str = None, author: str = None) -> dict:
        """
        Generate QR code data
        
        Returns data that can be encoded in a QR code
        """
        verification_url = self.generate_verification_url(tx_id)
        
        qr_payload = {
            "type": "brainblock_proof",
            "version": "1.0",
            "tx_id": tx_id,
            "verification_url": verification_url,
            "title": title,
            "author": author,
            "generated_at": datetime.datetime.now().isoformat()
        }
        
        return qr_payload
    
    def generate_qr_ascii(self, data: str, size: int = 21) -> str:
        """
        Generate ASCII art QR code (simplified visualization)
        
        In production, use qrcode library for actual QR codes
        """
        # Create deterministic pattern based on data hash
        hash_val = hashlib.md5(data.encode()).hexdigest()
        
        # Build simplified QR-like pattern
        lines = []
        
        # Top border with finder pattern
        lines.append("█" * (size + 8))
        lines.append("█" + "░" * (size + 6) + "█")
        lines.append("█" + "░" + "█" * 5 + "░" * (size - 6) + "█" * 5 + "░" + "█")
        lines.append("█" + "░" + "█░█░█" + "░" * (size - 6) + "█░█░█" + "░" + "█")
        lines.append("█" + "░" + "█" * 5 + "░" * (size - 6) + "█" * 5 + "░" + "█")
        lines.append("█" + "░" * (size + 6) + "█")
        
        # Data area with hash-based pattern
        for i in range(size - 6):
            row = "█░"
            for j in range(size + 2):
                # Use hash to determine block
                idx = (i * size + j) % len(hash_val)
                char_val = int(hash_val[idx], 16)
                row += "█" if char_val > 7 else "░"
            row += "░█"
            lines.append(row)
        
        # Bottom border
        lines.append("█" + "░" * (size + 6) + "█")
        lines.append("█" * (size + 8))
        
        return "\n".join(lines)
    
    def generate_qr_html(self, tx_id: str, title: str = None) -> str:
        """Generate HTML with embedded QR code"""
        verification_url = self.generate_verification_url(tx_id)
        
        # Using Google Charts API for QR code generation
        qr_image_url = f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={verification_url}"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>BrainBlock Proof - {title or tx_id[:12]}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }}
        .card {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 400px;
        }}
        .logo {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        h1 {{
            color: #333;
            font-size: 24px;
            margin: 10px 0;
        }}
        .qr-code {{
            margin: 20px 0;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
        }}
        .qr-code img {{
            max-width: 200px;
        }}
        .tx-id {{
            font-family: monospace;
            font-size: 12px;
            color: #666;
            word-break: break-all;
            background: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .verify-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 30px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-top: 15px;
        }}
        .verify-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }}
        .badge {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">🧠</div>
        <h1>BrainBlock Proof</h1>
        <p>{title or 'Intellectual Property Protected'}</p>
        
        <div class="qr-code">
            <img src="{qr_image_url}" alt="Scan to verify">
            <p style="margin: 10px 0 0 0; font-size: 12px; color: #888;">
                Scan to verify on blockchain
            </p>
        </div>
        
        <div class="tx-id">
            <strong>Transaction ID:</strong><br>
            {tx_id}
        </div>
        
        <span class="badge">✓ Verified on Algorand</span>
        
        <br>
        <a href="{verification_url}" class="verify-btn" target="_blank">
            View on Explorer →
        </a>
    </div>
</body>
</html>
        """
        return html
    
    def generate_shareable_link(self, tx_id: str) -> dict:
        """Generate shareable links for different platforms"""
        verification_url = self.generate_verification_url(tx_id)
        
        return {
            "direct": verification_url,
            "twitter": f"https://twitter.com/intent/tweet?text=Check%20out%20my%20blockchain-verified%20innovation!%20%F0%9F%A7%A0%E2%9B%93%20&url={verification_url}&hashtags=BrainBlock,Algorand,Hackathon",
            "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={verification_url}",
            "email": f"mailto:?subject=My%20BrainBlock%20Proof&body=I've%20registered%20my%20innovation%20on%20the%20blockchain!%0A%0AVerify%20here:%20{verification_url}",
            "whatsapp": f"https://wa.me/?text=Check%20out%20my%20blockchain-verified%20innovation!%20{verification_url}",
            "telegram": f"https://t.me/share/url?url={verification_url}&text=My%20BrainBlock%20Proof"
        }


class CertificateGenerator:
    """
    Generate ownership certificates
    """
    
    CERTIFICATE_TEMPLATE_ASCII = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ██████╗  █████╗ ██╗███╗   ██╗██████╗ ██╗      ██████╗  ██████╗██╗  ██╗   ║
║   ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝   ║
║   ██████╔╝██████╔╝███████║██║██╔██╗ ██║██████╔╝██║     ██║   ██║██║     █████╔╝    ║
║   ██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗    ║
║   ██████╔╝██║  ██║██║  ██║██║██║ ╚████║██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗   ║
║   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ║
║                                                                              ║
║                    CERTIFICATE OF INTELLECTUAL PROPERTY                      ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   This certifies that                                                        ║
║                                                                              ║
║                          {author:^40}                              ║
║                                                                              ║
║   is the verified creator and owner of                                       ║
║                                                                              ║
║                          {title:^40}                              ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   Certificate ID:    {cert_id:<52}   ║
║   Transaction ID:    {tx_id:<52}   ║
║   Block Number:      {block:<52}   ║
║   Timestamp:         {timestamp:<52}   ║
║   Network:           {network:<52}   ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   Verification URL:                                                          ║
║   {url:<72}   ║
║                                                                              ║
║   ✓ Immutably recorded on Algorand blockchain                                ║
║   ✓ Cryptographically verified ownership                                     ║
║   ✓ Timestamp cannot be altered or backdated                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    
    def __init__(self):
        self.qr_generator = QRCodeGenerator()
    
    def generate_certificate_id(self, tx_id: str) -> str:
        """Generate unique certificate ID"""
        hash_val = hashlib.sha256(tx_id.encode()).hexdigest()[:8].upper()
        return f"BB-{hash_val}-{datetime.datetime.now().strftime('%Y%m%d')}"
    
    def generate_ascii_certificate(self, 
                                   title: str,
                                   author: str,
                                   tx_id: str,
                                   block: int,
                                   timestamp: str,
                                   network: str = "Algorand Testnet") -> str:
        """Generate ASCII text certificate"""
        cert_id = self.generate_certificate_id(tx_id)
        url = self.qr_generator.generate_verification_url(tx_id)
        
        certificate = self.CERTIFICATE_TEMPLATE_ASCII.format(
            author=author[:40],
            title=title[:40],
            cert_id=cert_id,
            tx_id=tx_id[:52],
            block=str(block),
            timestamp=timestamp[:52],
            network=network,
            url=url[:72]
        )
        
        return certificate
    
    def generate_html_certificate(self,
                                  title: str,
                                  author: str,
                                  tx_id: str,
                                  block: int,
                                  timestamp: str,
                                  ownership_percentage: float = 100.0,
                                  network: str = "Algorand Testnet") -> str:
        """Generate HTML certificate"""
        cert_id = self.generate_certificate_id(tx_id)
        verification_url = self.qr_generator.generate_verification_url(tx_id)
        qr_image_url = f"https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={verification_url}"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>BrainBlock Certificate - {title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px;
        }}
        
        .certificate {{
            width: 800px;
            background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 30px 60px rgba(0,0,0,0.4);
            position: relative;
        }}
        
        .certificate::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 8px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .logo {{
            font-size: 64px;
            margin-bottom: 10px;
        }}
        
        .brand {{
            font-family: 'Playfair Display', serif;
            font-size: 36px;
            letter-spacing: 2px;
        }}
        
        .cert-title {{
            font-size: 18px;
            opacity: 0.9;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 4px;
        }}
        
        .body {{
            padding: 40px;
        }}
        
        .certifies {{
            text-align: center;
            color: #666;
            font-size: 16px;
            margin-bottom: 10px;
        }}
        
        .author {{
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            color: #333;
            padding: 15px 0;
            border-bottom: 2px solid #667eea;
            margin: 0 100px 20px;
        }}
        
        .project-label {{
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 20px;
        }}
        
        .project {{
            text-align: center;
            font-size: 24px;
            font-weight: 600;
            color: #333;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 10px;
            margin: 10px 50px;
        }}
        
        .ownership {{
            text-align: center;
            margin: 20px 0;
        }}
        
        .ownership-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 10px 30px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: 600;
        }}
        
        .details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
            background: #fafafa;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .detail-item {{
            padding: 10px;
        }}
        
        .detail-label {{
            color: #888;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .detail-value {{
            color: #333;
            font-size: 14px;
            font-weight: 600;
            word-break: break-all;
            margin-top: 5px;
        }}
        
        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 30px 40px;
            background: #f5f5f5;
            border-top: 1px solid #eee;
        }}
        
        .qr-section {{
            text-align: center;
        }}
        
        .qr-section img {{
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .qr-label {{
            font-size: 12px;
            color: #888;
            margin-top: 10px;
        }}
        
        .verification {{
            text-align: right;
        }}
        
        .verified-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #e8f5e9;
            color: #2e7d32;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }}
        
        .verify-link {{
            display: block;
            color: #667eea;
            font-size: 12px;
            margin-top: 10px;
            text-decoration: none;
        }}
        
        .watermark {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 120px;
            opacity: 0.03;
            font-weight: bold;
            pointer-events: none;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .certificate {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="certificate">
        <div class="watermark">BRAINBLOCK</div>
        
        <div class="header">
            <div class="logo">🧠</div>
            <div class="brand">BRAINBLOCK</div>
            <div class="cert-title">Certificate of Intellectual Property</div>
        </div>
        
        <div class="body">
            <p class="certifies">This is to certify that</p>
            <div class="author">{author}</div>
            
            <p class="project-label">is the verified owner of</p>
            <div class="project">{title}</div>
            
            <div class="ownership">
                <span class="ownership-badge">{ownership_percentage}% Ownership</span>
            </div>
            
            <div class="details">
                <div class="detail-item">
                    <div class="detail-label">Certificate ID</div>
                    <div class="detail-value">{cert_id}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Issue Date</div>
                    <div class="detail-value">{datetime.datetime.now().strftime('%B %d, %Y')}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Transaction ID</div>
                    <div class="detail-value">{tx_id}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Block Number</div>
                    <div class="detail-value">{block}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Timestamp</div>
                    <div class="detail-value">{timestamp}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Network</div>
                    <div class="detail-value">{network}</div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="qr-section">
                <img src="{qr_image_url}" alt="QR Code" width="100" height="100">
                <div class="qr-label">Scan to verify</div>
            </div>
            <div class="verification">
                <span class="verified-badge">
                    ✓ Blockchain Verified
                </span>
                <a href="{verification_url}" class="verify-link" target="_blank">
                    View on Algorand Explorer →
                </a>
            </div>
        </div>
    </div>
</body>
</html>
        """
        return html
    
    def generate_json_certificate(self,
                                  title: str,
                                  author: str,
                                  tx_id: str,
                                  block: int,
                                  timestamp: str,
                                  ownership_percentage: float = 100.0,
                                  network: str = "Algorand Testnet") -> dict:
        """Generate JSON certificate data"""
        cert_id = self.generate_certificate_id(tx_id)
        verification_url = self.qr_generator.generate_verification_url(tx_id)
        
        return {
            "certificate": {
                "id": cert_id,
                "type": "BrainBlock IP Certificate",
                "version": "1.0",
                "issued_at": datetime.datetime.now().isoformat()
            },
            "owner": {
                "name": author,
                "ownership_percentage": ownership_percentage
            },
            "project": {
                "title": title
            },
            "blockchain": {
                "network": network,
                "transaction_id": tx_id,
                "block_number": block,
                "timestamp": timestamp,
                "verification_url": verification_url
            },
            "verification": {
                "status": "verified",
                "method": "Algorand blockchain lookup",
                "immutable": True
            },
            "share_links": self.qr_generator.generate_shareable_link(tx_id)
        }


def demo_qr_and_certificate():
    """Demo the QR and certificate generation"""
    print("\n" + "="*60)
    print("🔲 QR CODE & CERTIFICATE GENERATOR DEMO")
    print("="*60)
    
    # Sample data
    tx_id = "ABCD1234EFGH5678IJKL9012MNOP3456QRST7890UVWX1234ABCD"
    title = "AI-Powered Innovation Detection System"
    author = "Alice Johnson"
    block = 35123456
    timestamp = datetime.datetime.now().isoformat()
    
    # QR Code
    qr = QRCodeGenerator()
    print("\n📱 QR Code Data:")
    print("-" * 40)
    qr_data = qr.generate_qr_data(tx_id, title, author)
    for key, value in qr_data.items():
        print(f"  {key}: {value}")
    
    print("\n🔗 Shareable Links:")
    print("-" * 40)
    links = qr.generate_shareable_link(tx_id)
    for platform, link in links.items():
        print(f"  {platform}: {link[:60]}...")
    
    # ASCII QR
    print("\n📊 ASCII QR Code:")
    print("-" * 40)
    ascii_qr = qr.generate_qr_ascii(tx_id, size=15)
    print(ascii_qr)
    
    # Certificate
    cert = CertificateGenerator()
    print("\n📜 ASCII Certificate:")
    print("-" * 40)
    ascii_cert = cert.generate_ascii_certificate(
        title=title,
        author=author,
        tx_id=tx_id,
        block=block,
        timestamp=timestamp
    )
    print(ascii_cert)
    
    print("\n✅ HTML and JSON certificates also available!")
    print("="*60)


if __name__ == "__main__":
    demo_qr_and_certificate()
