"""
BrainBlock: Student IP & Project Timestamp System
A comprehensive model demonstrating AI fingerprinting + blockchain timestamping

Tech Stack:
- AI/ML: Transformer embeddings, NLP, novelty detection
- Blockchain: Algorand (smart contracts, transactions)
- Cloud: AWS (S3, DynamoDB, Lambda, SQS, Cognito, API Gateway)
- Integrations: GitHub, Devpost, MLH
- Auth: Web3/WalletConnect, OAuth
- Notifications: Email (SES), Push (FCM), Webhooks, Slack, Discord
"""

import hashlib
import json
import datetime
from typing import Optional, List
from dataclasses import dataclass, asdict
from fingerprint import generate_fingerprint, extract_keywords
from blockchain import AlgorandSimulator
from plagiarism import check_originality
from ai_engine import AIEngine, NoveltyDetector
from aws_cloud import AWSCloud
from integrations import IntegrationHub
from wallet import WalletHub
from notifications import NotificationHub
from analytics import DashboardMetrics, AnalyticsEngine


@dataclass
class Submission:
    """Represents a student's project submission"""
    title: str
    content: str
    author: str
    wallet_address: str
    timestamp: str = ""
    content_hash: str = ""
    fingerprint: dict = None
    originality_score: float = 0.0
    blockchain_tx: str = ""
    
    def __post_init__(self):
        self.timestamp = datetime.datetime.now().isoformat()
        self.content_hash = self._generate_hash()
        
    def _generate_hash(self) -> str:
        """Generate SHA-256 hash of the content"""
        combined = f"{self.title}|{self.content}|{self.author}|{self.timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()


@dataclass 
class Contributor:
    """Represents a contributor in a group project"""
    name: str
    wallet_address: str
    contribution: str
    contribution_type: str  # 'algorithm', 'implementation', 'design', 'docs'
    ownership_percentage: float = 0.0
    fingerprint: str = ""


class BrainBlock:
    """Main BrainBlock system for IP protection with full tech stack"""
    
    def __init__(self, enable_cloud: bool = True):
        # Core services
        self.blockchain = AlgorandSimulator()
        self.ai = AIEngine()
        
        # Cloud & infrastructure
        self.cloud = AWSCloud() if enable_cloud else None
        
        # Integrations
        self.integrations = IntegrationHub()
        self.wallet = WalletHub()
        self.notifications = NotificationHub()
        
        # Analytics
        self.analytics = AnalyticsEngine()
        self.dashboard = DashboardMetrics()
        
        # Data
        self.submissions = []
        
    def submit_project(self, title: str, content: str, author: str, wallet: str,
                       email: Optional[str] = None) -> dict:
        """
        Submit a project for IP protection
        Returns submission result with blockchain proof
        """
        print(f"\n{'='*60}")
        print(f"🧠 BRAINBLOCK: Processing submission...")
        print(f"{'='*60}")
        
        # Track analytics event
        self.analytics.track_event("submission_started", {"title": title})
        
        # Step 1: Create submission
        submission = Submission(
            title=title,
            content=content,
            author=author,
            wallet_address=wallet
        )
        print(f"\n✅ Step 1: Submission created")
        print(f"   Title: {title}")
        print(f"   Author: {author}")
        print(f"   Hash: {submission.content_hash[:16]}...")
        
        # Step 2: Advanced AI Analysis
        print(f"\n🤖 Step 2: Advanced AI Analysis...")
        ai_result = self.ai.full_analysis(content)
        fingerprint = generate_fingerprint(content)
        submission.fingerprint = fingerprint
        
        print(f"   Embedding: {ai_result['embedding']['model']} ({ai_result['embedding']['dimensions']}d)")
        print(f"   Novelty Score: {ai_result['novelty']['score']:.2f}")
        print(f"   Innovations Found: {ai_result['nlp']['innovations_found']}")
        print(f"   Keywords: {', '.join(fingerprint['keywords'][:5])}")
        if ai_result['code']:
            print(f"   Code Language: {ai_result['code']['language']}")
        
        # Step 3: Plagiarism Check
        print(f"\n🔎 Step 3: Originality Check...")
        originality = check_originality(content)
        submission.originality_score = originality['score']
        print(f"   Originality Score: {originality['score']:.1%}")
        print(f"   Status: {originality['status']}")
        
        if originality['score'] < 0.7:
            print(f"\n❌ REJECTED: Content does not meet originality threshold")
            self.analytics.track_event("submission_rejected", {"reason": "originality"})
            return {
                "success": False,
                "reason": "Failed originality check",
                "score": originality['score']
            }
        
        # Step 4: Cloud Storage (if enabled)
        if self.cloud:
            print(f"\n☁️  Step 4: Storing in AWS Cloud...")
            s3_result = self.cloud.s3.upload_submission(
                submission_id=submission.content_hash[:16],
                content=content.encode(),
                metadata={"title": title, "author": author}
            )
            print(f"   S3: {s3_result['url']}")
            
            # Store in DynamoDB
            self.cloud.dynamodb.put_record({
                "pk": submission.content_hash[:16],
                "title": title,
                "author": author,
                "wallet": wallet,
                "originality": originality['score']
            })
            print(f"   DynamoDB: Record stored")
        
        # Step 5: Blockchain Registration
        print(f"\n⛓️  Step 5: Registering on Algorand Blockchain...")
        tx_result = self.blockchain.create_transaction(
            sender=wallet,
            metadata={
                "type": "brainblock_ip_registration",
                "title": title,
                "author": author,
                "content_hash": submission.content_hash,
                "fingerprint_hash": hashlib.sha256(
                    json.dumps(fingerprint).encode()
                ).hexdigest(),
                "originality_score": originality['score'],
                "ai_novelty_score": ai_result['novelty']['score'],
                "timestamp": submission.timestamp
            }
        )
        submission.blockchain_tx = tx_result['tx_id']
        
        print(f"   Transaction ID: {tx_result['tx_id']}")
        print(f"   Block: {tx_result['block']}")
        print(f"   Explorer: {tx_result['explorer_url']}")
        
        self.submissions.append(submission)
        
        # Step 6: Send Notifications
        if email:
            print(f"\n📧 Step 6: Sending Notifications...")
            self.notifications.notify_submission_confirmed(
                user_data={"email": email, "name": author},
                submission_data={
                    "title": title,
                    "tx_id": tx_result['tx_id'],
                    "block": tx_result['block'],
                    "timestamp": submission.timestamp,
                    "explorer_url": tx_result['explorer_url']
                }
            )
            print(f"   Email sent to {email}")
        
        # Track success
        self.analytics.track_event("submission_completed", {
            "title": title, 
            "tx_id": tx_result['tx_id']
        })
        
        # Final Result
        print(f"\n{'='*60}")
        print(f"🎉 SUCCESS: Your innovation is now protected!")
        print(f"{'='*60}")
        
        return {
            "success": True,
            "submission": asdict(submission),
            "ai_analysis": ai_result,
            "blockchain": tx_result,
            "proof_url": tx_result['explorer_url']
        }
    
    def submit_group_project(self, title: str, contributors: List[Contributor]) -> dict:
        """
        Submit a group project with multiple contributors
        Uses smart contracts for ownership distribution
        """
        print(f"\n{'='*60}")
        print(f"🧠 BRAINBLOCK CO-CREATOR VAULT: Processing group submission...")
        print(f"{'='*60}")
        
        # Track analytics
        self.analytics.track_event("group_submission_started", {
            "title": title, 
            "contributors": len(contributors)
        })
        
        # Analyze each contributor with advanced AI
        print(f"\n👥 Step 1: Analyzing {len(contributors)} contributors...")
        
        total_novelty = 0
        analyzed_contributors = []
        
        for contrib in contributors:
            # Use advanced AI analysis
            ai_result = self.ai.full_analysis(contrib.contribution)
            fingerprint = generate_fingerprint(contrib.contribution)
            
            contrib.fingerprint = hashlib.sha256(
                json.dumps(fingerprint).encode()
            ).hexdigest()[:16]
            
            novelty = ai_result['novelty']['score']
            total_novelty += novelty
            analyzed_contributors.append((contrib, novelty, ai_result))
            
            print(f"\n   📝 {contrib.name} ({contrib.contribution_type})")
            print(f"      Novelty Score: {novelty:.2f}")
            print(f"      Innovations: {ai_result['nlp']['innovations_found']}")
            print(f"      Fingerprint: {contrib.fingerprint}...")
        
        # Calculate fair ownership split based on AI analysis
        print(f"\n⚖️  Step 2: AI-Calculated Fair Split:")
        for contrib, novelty, _ in analyzed_contributors:
            if total_novelty > 0:
                contrib.ownership_percentage = round((novelty / total_novelty) * 100, 1)
            else:
                contrib.ownership_percentage = round(100 / len(contributors), 1)
            print(f"   {contrib.name}: {contrib.ownership_percentage}%")
        
        # Store in cloud if enabled
        if self.cloud:
            print(f"\n☁️  Step 3: Storing in AWS Cloud...")
            for contrib in contributors:
                self.cloud.dynamodb.put_record({
                    "pk": f"group_{title}_{contrib.name}",
                    "project": title,
                    "contributor": contrib.name,
                    "ownership": contrib.ownership_percentage,
                    "type": contrib.contribution_type
                })
            print(f"   {len(contributors)} contributor records stored")
        
        # Create smart contract transaction
        print(f"\n⛓️  Step 4: Creating Smart Contract on Algorand...")
        
        contract_data = {
            "type": "brainblock_group_ip",
            "title": title,
            "contributors": [
                {
                    "name": c.name,
                    "wallet": c.wallet_address,
                    "ownership": c.ownership_percentage,
                    "type": c.contribution_type,
                    "fingerprint": c.fingerprint
                }
                for c in contributors
            ],
            "total_ownership": 100,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        tx_result = self.blockchain.create_smart_contract(contract_data)
        
        print(f"   Contract ID: {tx_result['contract_id']}")
        print(f"   Transaction: {tx_result['tx_id']}")
        print(f"   Explorer: {tx_result['explorer_url']}")
        
        # Track success
        self.analytics.track_event("group_submission_completed", {
            "title": title,
            "contract_id": tx_result['contract_id']
        })
        
        print(f"\n{'='*60}")
        print(f"🎉 GROUP PROJECT PROTECTED WITH SMART CONTRACT!")
        print(f"{'='*60}")
        
        return {
            "success": True,
            "contract_id": tx_result['contract_id'],
            "contributors": [asdict(c) for c in contributors],
            "blockchain": tx_result
        }
    
    def verify_ownership(self, tx_id: str) -> dict:
        """Verify ownership using blockchain transaction ID"""
        return self.blockchain.verify_transaction(tx_id)
    
    def import_from_github(self, repo_url: str) -> dict:
        """Import project from GitHub for registration"""
        return self.integrations.import_from_github(repo_url)
    
    def connect_wallet(self, wallet_type: str = "pera") -> dict:
        """Connect user's wallet"""
        return self.wallet.connect(wallet_type)
    
    def get_dashboard_stats(self) -> dict:
        """Get platform statistics"""
        return self.dashboard.get_overview()
    
    def get_aws_infrastructure(self) -> dict:
        """Get AWS infrastructure summary"""
        if self.cloud:
            return self.cloud.get_infrastructure_summary()
        return {"error": "Cloud not enabled"}


# Demo runner
if __name__ == "__main__":
    from demo import run_demo
    run_demo()
