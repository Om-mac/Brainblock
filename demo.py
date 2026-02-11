"""
BrainBlock Demo
Run this to see BrainBlock in action
"""

from main import BrainBlock, Contributor


def run_demo():
    """Run a complete demo of BrainBlock features"""
    
    print("\n" + "="*70)
    print("       🧠 BRAINBLOCK DEMO: Student IP Protection System")
    print("="*70)
    
    brainblock = BrainBlock()
    
    # ============================================
    # DEMO 1: Single Student Project Submission
    # ============================================
    print("\n\n" + "─"*70)
    print("📌 DEMO 1: Individual Project Submission")
    print("─"*70)
    
    sample_project = """
    Project: Neural Network-Based Plagiarism Detection System
    
    Our novel approach combines transformer-based embeddings with 
    blockchain verification to create an immutable record of original work.
    
    Key Innovation:
    - Custom BERT fine-tuned on academic papers
    - Real-time similarity scoring using cosine distance
    - Algorand smart contracts for timestamp verification
    
    Implementation:
    def detect_plagiarism(text):
        embeddings = model.encode(text)
        similarity = compare_with_database(embeddings)
        if similarity < threshold:
            register_on_blockchain(text)
        return similarity
    
    This system provides 99.2% accuracy on benchmark datasets while
    maintaining sub-second response times.
    """
    
    result = brainblock.submit_project(
        title="AI-Powered Plagiarism Detection with Blockchain Verification",
        content=sample_project,
        author="Alice Johnson",
        wallet="ALGO7X3K2M4N5P6Q8R9S0T1U2V3W4X5Y6Z7A8B9C0D1E2F3G4H5I6J"
    )
    
    if result['success']:
        print(f"\n📋 Proof URL: {result['proof_url']}")
        print(f"   (Share this link to prove ownership!)")
    
    # ============================================
    # DEMO 2: Group Project with Multiple Contributors
    # ============================================
    print("\n\n" + "─"*70)
    print("📌 DEMO 2: Group Project - Co-Creator Vault")
    print("─"*70)
    
    contributors = [
        Contributor(
            name="Bob Smith",
            wallet_address="ALGOBOB123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ012345678",
            contribution="""
            Core Algorithm Design:
            Developed the novel consensus mechanism that reduces 
            blockchain confirmation time by 40% using a hybrid 
            proof-of-stake approach. Implemented custom hash function
            optimized for IoT devices with limited computing power.
            
            class HybridConsensus:
                def validate_block(self, block):
                    stake_check = self.verify_stake(block.validator)
                    hash_check = self.verify_hash(block.hash)
                    return stake_check and hash_check
            """,
            contribution_type="algorithm"
        ),
        Contributor(
            name="Carol White",
            wallet_address="ALGOCAROL98765432ZYXWVUTSRQPONMLKJIHGFEDCBA987654",
            contribution="""
            Frontend Implementation:
            Built the React-based dashboard for monitoring blockchain
            transactions. Implemented real-time updates using WebSockets
            and created user-friendly visualizations with D3.js.
            
            const TransactionMonitor = () => {
                const [txs, setTxs] = useState([]);
                useEffect(() => {
                    socket.on('new_tx', (tx) => setTxs([...txs, tx]));
                }, []);
                return <TxChart data={txs} />;
            };
            """,
            contribution_type="implementation"
        ),
        Contributor(
            name="David Lee",
            wallet_address="ALGODAVID456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            contribution="""
            Documentation and Testing:
            Wrote comprehensive API documentation and created
            unit tests achieving 95% code coverage. Set up CI/CD
            pipeline with GitHub Actions.
            """,
            contribution_type="docs"
        )
    ]
    
    group_result = brainblock.submit_group_project(
        title="HybridChain: Fast Consensus for IoT Blockchain",
        contributors=contributors
    )
    
    if group_result['success']:
        print(f"\n📋 Smart Contract ID: {group_result['contract_id']}")
        print(f"\n👥 Ownership Distribution (AI-Verified):")
        for contrib in group_result['contributors']:
            print(f"   • {contrib['name']}: {contrib['ownership_percentage']}%")
    
    # ============================================
    # DEMO 3: Verification
    # ============================================
    print("\n\n" + "─"*70)
    print("📌 DEMO 3: Ownership Verification")
    print("─"*70)
    
    if result['success']:
        tx_id = result['blockchain']['tx_id']
        print(f"\nVerifying transaction: {tx_id[:20]}...")
        
        verification = brainblock.verify_ownership(tx_id)
        if verification['verified']:
            print(f"✅ {verification['message']}")
            print(f"   Block: {verification['transaction']['block']}")
            print(f"   Timestamp: {verification['transaction']['timestamp']}")
    
    # ============================================
    # Summary
    # ============================================
    print("\n\n" + "="*70)
    print("                    ✨ DEMO COMPLETE ✨")
    print("="*70)
    print("""
    What we demonstrated:
    
    1. 📄 INDIVIDUAL IP PROTECTION
       - AI analyzed project content
       - Generated unique fingerprint
       - Checked originality (plagiarism scan)
       - Created immutable blockchain record
    
    2. 👥 GROUP PROJECT COLLABORATION
       - Analyzed each contributor's work
       - AI suggested fair ownership split
       - Deployed smart contract with percentages
       - Created dispute-proof ownership record
    
    3. ✅ VERIFICATION
       - Anyone can verify ownership
       - Blockchain proof is publicly accessible
       - No intermediaries needed
    
    For production deployment:
    - Replace blockchain simulator with algosdk
    - Integrate real plagiarism APIs (Turnitin/Copyleaks)
    - Add user authentication with wallet connect
    - Deploy smart contracts to Algorand mainnet
    """)


if __name__ == "__main__":
    run_demo()
