"""
BrainBlock REST API
Flask-based API for web and mobile integrations
"""

import json
import datetime
from functools import wraps
from dataclasses import asdict

# Simulated Flask-like API (for demo without dependencies)
# In production, use actual Flask


class Request:
    """Simulated request object"""
    def __init__(self, json_data=None, headers=None, args=None):
        self.json = json_data or {}
        self.headers = headers or {}
        self.args = args or {}


class Response:
    """API Response wrapper"""
    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {'Content-Type': 'application/json'}
        
    def to_json(self):
        return json.dumps(self.data, indent=2, default=str)


def jsonify(data, status=200):
    """Convert data to JSON response"""
    return Response(data, status)


def api_response(success=True, data=None, message=None, error=None, status=200):
    """Standard API response format"""
    response = {
        "success": success,
        "timestamp": datetime.datetime.now().isoformat(),
        "data": data,
    }
    if message:
        response["message"] = message
    if error:
        response["error"] = error
        response["success"] = False
    return jsonify(response, status)


class BrainBlockAPI:
    """
    REST API for BrainBlock
    
    Endpoints:
    - POST /api/v1/submit - Submit individual project
    - POST /api/v1/submit/group - Submit group project
    - GET /api/v1/verify/<tx_id> - Verify ownership
    - GET /api/v1/proof/<tx_id> - Get proof certificate
    - GET /api/v1/stats - Platform statistics
    - POST /api/v1/wallet/connect - Connect wallet
    - GET /api/v1/projects - List user projects
    """
    
    VERSION = "1.0.0"
    API_PREFIX = "/api/v1"
    
    def __init__(self):
        from main import BrainBlock, Contributor
        self.brainblock = BrainBlock()
        self.Contributor = Contributor
        self.routes = self._register_routes()
        
    def _register_routes(self):
        """Register API routes"""
        return {
            ("GET", "/"): self.root,
            ("GET", "/health"): self.health_check,
            ("GET", "/api/v1"): self.api_info,
            ("POST", "/api/v1/submit"): self.submit_project,
            ("POST", "/api/v1/submit/group"): self.submit_group_project,
            ("GET", "/api/v1/verify"): self.verify_ownership,
            ("GET", "/api/v1/proof"): self.get_proof,
            ("GET", "/api/v1/stats"): self.get_stats,
            ("POST", "/api/v1/wallet/connect"): self.connect_wallet,
            ("GET", "/api/v1/projects"): self.list_projects,
            ("POST", "/api/v1/analyze"): self.analyze_content,
            ("GET", "/api/v1/certificate"): self.generate_certificate,
        }
    
    def root(self, request):
        """Root endpoint"""
        return api_response(
            success=True,
            data={
                "name": "BrainBlock API",
                "version": self.VERSION,
                "description": "Student IP Protection with AI + Blockchain",
                "endpoints": {
                    "api_info": f"{self.API_PREFIX}",
                    "submit": f"{self.API_PREFIX}/submit",
                    "submit_group": f"{self.API_PREFIX}/submit/group",
                    "verify": f"{self.API_PREFIX}/verify?tx_id=<id>",
                    "stats": f"{self.API_PREFIX}/stats",
                }
            },
            message="Welcome to BrainBlock API"
        )
    
    def health_check(self, request):
        """Health check endpoint"""
        return api_response(
            success=True,
            data={
                "status": "healthy",
                "version": self.VERSION,
                "uptime": "99.97%",
                "services": {
                    "ai_engine": "operational",
                    "blockchain": "operational",
                    "cloud": "operational"
                }
            }
        )
    
    def api_info(self, request):
        """API documentation"""
        return api_response(
            success=True,
            data={
                "version": self.VERSION,
                "base_url": self.API_PREFIX,
                "endpoints": [
                    {
                        "method": "POST",
                        "path": "/submit",
                        "description": "Submit individual project for IP protection",
                        "body": {
                            "title": "string (required)",
                            "content": "string (required)",
                            "author": "string (required)",
                            "wallet_address": "string (required)",
                            "email": "string (optional)"
                        }
                    },
                    {
                        "method": "POST",
                        "path": "/submit/group",
                        "description": "Submit group project with ownership split",
                        "body": {
                            "title": "string (required)",
                            "contributors": [
                                {
                                    "name": "string",
                                    "wallet_address": "string",
                                    "contribution": "string",
                                    "contribution_type": "algorithm|implementation|design|docs"
                                }
                            ]
                        }
                    },
                    {
                        "method": "GET",
                        "path": "/verify",
                        "description": "Verify ownership by transaction ID",
                        "params": {"tx_id": "string"}
                    },
                    {
                        "method": "GET",
                        "path": "/stats",
                        "description": "Get platform statistics"
                    },
                    {
                        "method": "POST",
                        "path": "/analyze",
                        "description": "Analyze content without registering",
                        "body": {"content": "string"}
                    }
                ],
                "authentication": "Bearer token (optional for demo)",
                "rate_limit": "100 requests/minute"
            }
        )
    
    def submit_project(self, request):
        """
        Submit individual project
        
        POST /api/v1/submit
        {
            "title": "Project Title",
            "content": "Project description and code...",
            "author": "Author Name",
            "wallet_address": "ALGO...",
            "email": "optional@email.com"
        }
        """
        data = request.json
        
        # Validate required fields
        required = ['title', 'content', 'author', 'wallet_address']
        missing = [f for f in required if not data.get(f)]
        
        if missing:
            return api_response(
                success=False,
                error=f"Missing required fields: {', '.join(missing)}",
                status=400
            )
        
        try:
            result = self.brainblock.submit_project(
                title=data['title'],
                content=data['content'],
                author=data['author'],
                wallet=data['wallet_address'],
                email=data.get('email')
            )
            
            if result['success']:
                return api_response(
                    success=True,
                    data={
                        "submission": result['submission'],
                        "blockchain": result['blockchain'],
                        "ai_analysis": {
                            "novelty_score": result['ai_analysis']['novelty']['score'],
                            "innovations_found": result['ai_analysis']['nlp']['innovations_found'],
                            "keywords": result['ai_analysis']['nlp']['keywords'][:10]
                        },
                        "proof_url": result['proof_url']
                    },
                    message="Project successfully registered on blockchain"
                )
            else:
                return api_response(
                    success=False,
                    error=result.get('reason', 'Submission failed'),
                    data={"originality_score": result.get('score')},
                    status=400
                )
        except Exception as e:
            return api_response(
                success=False,
                error=str(e),
                status=500
            )
    
    def submit_group_project(self, request):
        """
        Submit group project
        
        POST /api/v1/submit/group
        {
            "title": "Group Project Title",
            "contributors": [
                {
                    "name": "Alice",
                    "wallet_address": "ALGO...",
                    "contribution": "Description...",
                    "contribution_type": "algorithm"
                }
            ]
        }
        """
        data = request.json
        
        if not data.get('title') or not data.get('contributors'):
            return api_response(
                success=False,
                error="Missing required fields: title, contributors",
                status=400
            )
        
        try:
            contributors = [
                self.Contributor(
                    name=c['name'],
                    wallet_address=c['wallet_address'],
                    contribution=c['contribution'],
                    contribution_type=c.get('contribution_type', 'implementation')
                )
                for c in data['contributors']
            ]
            
            result = self.brainblock.submit_group_project(
                title=data['title'],
                contributors=contributors
            )
            
            return api_response(
                success=True,
                data={
                    "contract_id": result['contract_id'],
                    "contributors": result['contributors'],
                    "blockchain": result['blockchain']
                },
                message="Group project registered with smart contract"
            )
        except Exception as e:
            return api_response(
                success=False,
                error=str(e),
                status=500
            )
    
    def verify_ownership(self, request):
        """
        Verify ownership
        
        GET /api/v1/verify?tx_id=<transaction_id>
        """
        tx_id = request.args.get('tx_id')
        
        if not tx_id:
            return api_response(
                success=False,
                error="Missing tx_id parameter",
                status=400
            )
        
        result = self.brainblock.verify_ownership(tx_id)
        
        return api_response(
            success=result['verified'],
            data=result,
            message=result['message']
        )
    
    def get_proof(self, request):
        """
        Get proof details
        
        GET /api/v1/proof?tx_id=<transaction_id>
        """
        tx_id = request.args.get('tx_id')
        
        if not tx_id:
            return api_response(
                success=False,
                error="Missing tx_id parameter",
                status=400
            )
        
        result = self.brainblock.verify_ownership(tx_id)
        
        if result['verified']:
            tx = result['transaction']
            proof_data = {
                "transaction_id": tx_id,
                "block_number": tx.get('block'),
                "timestamp": tx.get('timestamp'),
                "explorer_url": f"https://testnet.algoexplorer.io/tx/{tx_id}",
                "verified": True,
                "certificate": {
                    "type": "BrainBlock IP Certificate",
                    "standard": "Algorand ASA",
                    "network": "testnet"
                }
            }
            return api_response(success=True, data=proof_data)
        else:
            return api_response(
                success=False,
                error="Transaction not found",
                status=404
            )
    
    def get_stats(self, request):
        """
        Get platform statistics
        
        GET /api/v1/stats
        """
        stats = self.brainblock.get_dashboard_stats()
        return api_response(success=True, data=stats)
    
    def connect_wallet(self, request):
        """
        Connect wallet
        
        POST /api/v1/wallet/connect
        {"wallet_type": "pera|myalgo|algosigner"}
        """
        data = request.json
        wallet_type = data.get('wallet_type', 'pera')
        
        result = self.brainblock.connect_wallet(wallet_type)
        return api_response(
            success=True,
            data=result,
            message=f"Connected to {result['provider']}"
        )
    
    def list_projects(self, request):
        """
        List user's projects
        
        GET /api/v1/projects?wallet=<wallet_address>
        """
        wallet = request.args.get('wallet')
        
        # Return submissions for this wallet (simulated)
        projects = [
            asdict(s) for s in self.brainblock.submissions
            if not wallet or s.wallet_address == wallet
        ]
        
        return api_response(
            success=True,
            data={
                "total": len(projects),
                "projects": projects
            }
        )
    
    def analyze_content(self, request):
        """
        Analyze content without registering
        
        POST /api/v1/analyze
        {"content": "Your project content..."}
        """
        data = request.json
        content = data.get('content', '')
        
        if not content:
            return api_response(
                success=False,
                error="Content is required",
                status=400
            )
        
        # Run AI analysis only
        ai_result = self.brainblock.ai.full_analysis(content)
        
        from plagiarism import check_originality
        originality = check_originality(content)
        
        return api_response(
            success=True,
            data={
                "novelty_score": ai_result['novelty']['score'],
                "originality_score": originality['score'],
                "is_original": originality['score'] >= 0.7,
                "innovations_found": ai_result['nlp']['innovations_found'],
                "keywords": ai_result['nlp']['keywords'][:15],
                "code_detected": ai_result['code'] is not None,
                "code_language": ai_result['code']['language'] if ai_result['code'] else None,
                "recommendation": "Ready for registration" if originality['score'] >= 0.7 else "Content may need revision"
            }
        )
    
    def generate_certificate(self, request):
        """
        Generate ownership certificate
        
        GET /api/v1/certificate?tx_id=<id>&format=json|html
        """
        tx_id = request.args.get('tx_id')
        format_type = request.args.get('format', 'json')
        
        if not tx_id:
            return api_response(
                success=False,
                error="Missing tx_id parameter",
                status=400
            )
        
        result = self.brainblock.verify_ownership(tx_id)
        
        if not result['verified']:
            return api_response(
                success=False,
                error="Transaction not found",
                status=404
            )
        
        tx = result['transaction']
        
        certificate = {
            "certificate_id": f"BB-{tx_id[:12].upper()}",
            "type": "Intellectual Property Ownership Certificate",
            "issuer": "BrainBlock Platform",
            "issued_date": datetime.datetime.now().isoformat(),
            "blockchain": {
                "network": "Algorand Testnet",
                "transaction_id": tx_id,
                "block_number": tx.get('block'),
                "timestamp": tx.get('timestamp')
            },
            "verification_url": f"https://testnet.algoexplorer.io/tx/{tx_id}",
            "validity": "Perpetual - Immutable Blockchain Record",
            "qr_code_url": f"/api/v1/qr?tx_id={tx_id}"
        }
        
        return api_response(success=True, data=certificate)
    
    def handle_request(self, method, path, request):
        """Route handler"""
        route_key = (method.upper(), path)
        
        if route_key in self.routes:
            return self.routes[route_key](request)
        
        return api_response(
            success=False,
            error=f"Endpoint not found: {method} {path}",
            status=404
        )


# Flask app factory (for production)
def create_flask_app():
    """
    Create Flask application
    
    Usage:
        from api import create_flask_app
        app = create_flask_app()
        app.run(debug=True)
    """
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        api = BrainBlockAPI()
        
        @app.route('/')
        def root():
            result = api.root(request)
            return jsonify(result.data), result.status
        
        @app.route('/health')
        def health():
            result = api.health_check(request)
            return jsonify(result.data), result.status
        
        @app.route('/api/v1')
        def api_info():
            result = api.api_info(request)
            return jsonify(result.data), result.status
        
        @app.route('/api/v1/submit', methods=['POST'])
        def submit():
            result = api.submit_project(request)
            return jsonify(result.data), result.status
        
        @app.route('/api/v1/submit/group', methods=['POST'])
        def submit_group():
            result = api.submit_group_project(request)
            return jsonify(result.data), result.status
        
        @app.route('/api/v1/verify')
        def verify():
            result = api.verify_ownership(request)
            return jsonify(result.data), result.status
        
        @app.route('/api/v1/stats')
        def stats():
            result = api.get_stats(request)
            return jsonify(result.data), result.status
        
        @app.route('/api/v1/analyze', methods=['POST'])
        def analyze():
            result = api.analyze_content(request)
            return jsonify(result.data), result.status
        
        @app.route('/api/v1/certificate')
        def certificate():
            result = api.generate_certificate(request)
            return jsonify(result.data), result.status
        
        return app
        
    except ImportError:
        print("Flask not installed. Run: pip install flask flask-cors")
        return None


# Demo server
def run_demo_server():
    """Run demo API server"""
    print("\n" + "="*60)
    print("🌐 BRAINBLOCK API SERVER")
    print("="*60)
    
    api = BrainBlockAPI()
    
    print("\n📋 Available Endpoints:")
    print("-" * 40)
    
    for (method, path), _ in api.routes.items():
        print(f"  {method:6} {path}")
    
    print("\n" + "-" * 40)
    print("\n🔄 Simulating API Requests:\n")
    
    # Demo: Health check
    print("1. GET /health")
    result = api.handle_request("GET", "/health", Request())
    print(f"   Response: {result.data['data']['status']}")
    
    # Demo: Submit project
    print("\n2. POST /api/v1/submit")
    submit_request = Request(json_data={
        "title": "AI-Powered Code Review System",
        "content": "A novel machine learning approach to automated code review using transformer models...",
        "author": "Demo User",
        "wallet_address": "ALGO_DEMO_123"
    })
    result = api.handle_request("POST", "/api/v1/submit", submit_request)
    print(f"   Success: {result.data['success']}")
    if result.data['success']:
        print(f"   TX ID: {result.data['data']['blockchain']['tx_id'][:20]}...")
    
    # Demo: Get stats
    print("\n3. GET /api/v1/stats")
    result = api.handle_request("GET", "/api/v1/stats", Request())
    stats = result.data['data']
    print(f"   Total Submissions: {stats['total_submissions']}")
    print(f"   Total Users: {stats['total_users']}")
    
    print("\n" + "="*60)
    print("✅ API Demo Complete!")
    print("="*60)


if __name__ == "__main__":
    run_demo_server()
