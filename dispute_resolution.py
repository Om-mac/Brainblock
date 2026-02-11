"""
Dispute Resolution System
AI-powered fairness engine for ownership conflicts
"""

import hashlib
import datetime
import random
from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum


class DisputeStatus(Enum):
    """Dispute status"""
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    EVIDENCE_COLLECTION = "evidence_collection"
    AI_ANALYSIS = "ai_analysis"
    MEDIATION = "mediation"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    REJECTED = "rejected"


class DisputeType(Enum):
    """Types of disputes"""
    OWNERSHIP_CLAIM = "ownership_claim"
    CONTRIBUTION_PERCENTAGE = "contribution_percentage"
    PLAGIARISM_ACCUSATION = "plagiarism_accusation"
    TIMELINE_DISPUTE = "timeline_dispute"
    CO_CREATOR_CONFLICT = "co_creator_conflict"


class ResolutionOutcome(Enum):
    """Possible resolution outcomes"""
    ORIGINAL_UPHELD = "original_owner_upheld"
    CLAIMANT_UPHELD = "claimant_recognized"
    SHARED_OWNERSHIP = "shared_ownership_established"
    PERCENTAGE_ADJUSTED = "ownership_percentage_adjusted"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    REQUIRES_EXTERNAL_REVIEW = "requires_external_review"


@dataclass
class Evidence:
    """Evidence submitted for a dispute"""
    id: str
    dispute_id: str
    submitted_by: str
    evidence_type: str  # 'document', 'code', 'timestamp', 'witness', 'blockchain'
    description: str
    content_hash: str
    submitted_at: str
    verified: bool = False
    weight: float = 0.0  # AI-assigned evidence weight


@dataclass
class DisputeParty:
    """Party involved in a dispute"""
    wallet_address: str
    name: str
    role: str  # 'claimant', 'defendant', 'witness'
    evidence_submitted: List[str] = field(default_factory=list)
    claim_summary: str = ""


@dataclass
class Dispute:
    """Dispute case"""
    id: str
    type: DisputeType
    status: DisputeStatus
    original_tx_id: str
    project_title: str
    parties: List[DisputeParty]
    created_at: str
    updated_at: str
    timeline: List[dict] = field(default_factory=list)
    ai_analysis: dict = None
    resolution: dict = None
    blockchain_record: str = None


class AIFairnessEngine:
    """
    AI-powered fairness analysis for disputes
    
    Features:
    - Timeline analysis
    - Content similarity detection
    - Contribution assessment
    - Evidence credibility scoring
    """
    
    def __init__(self):
        self.weights = {
            'blockchain_timestamp': 0.35,  # Highest weight - immutable proof
            'code_similarity': 0.25,
            'documentation': 0.15,
            'commit_history': 0.15,
            'witness_testimony': 0.10
        }
    
    def analyze_dispute(self, dispute: Dispute, evidence_list: List[Evidence]) -> dict:
        """
        Perform comprehensive dispute analysis
        """
        print(f"\n🤖 AI FAIRNESS ENGINE: Analyzing dispute {dispute.id[:8]}...")
        
        analysis = {
            "dispute_id": dispute.id,
            "analysis_timestamp": datetime.datetime.now().isoformat(),
            "confidence": 0.0,
            "timeline_analysis": self._analyze_timeline(dispute, evidence_list),
            "similarity_analysis": self._analyze_similarity(evidence_list),
            "evidence_assessment": self._assess_evidence(evidence_list),
            "party_scores": {},
            "recommendation": None
        }
        
        # Calculate scores for each party
        for party in dispute.parties:
            if party.role in ['claimant', 'defendant']:
                score = self._calculate_party_score(party, evidence_list)
                analysis["party_scores"][party.wallet_address] = {
                    "name": party.name,
                    "role": party.role,
                    "score": score,
                    "evidence_count": len(party.evidence_submitted)
                }
        
        # Generate recommendation
        analysis["recommendation"] = self._generate_recommendation(analysis, dispute)
        analysis["confidence"] = self._calculate_confidence(analysis)
        
        return analysis
    
    def _analyze_timeline(self, dispute: Dispute, evidence_list: List[Evidence]) -> dict:
        """Analyze timestamps and chronology"""
        timestamps = []
        
        for evidence in evidence_list:
            if evidence.evidence_type in ['blockchain', 'timestamp']:
                timestamps.append({
                    "source": evidence.submitted_by,
                    "timestamp": evidence.submitted_at,
                    "type": evidence.evidence_type,
                    "verified": evidence.verified
                })
        
        # Sort by timestamp
        timestamps.sort(key=lambda x: x['timestamp'])
        
        earliest = timestamps[0] if timestamps else None
        
        return {
            "total_timestamps": len(timestamps),
            "verified_timestamps": sum(1 for t in timestamps if t['verified']),
            "earliest_record": earliest,
            "timeline_clear": len(set(t['source'] for t in timestamps[:3])) == 1 if timestamps else False
        }
    
    def _analyze_similarity(self, evidence_list: List[Evidence]) -> dict:
        """Analyze content similarity between submissions"""
        code_evidence = [e for e in evidence_list if e.evidence_type == 'code']
        
        if len(code_evidence) < 2:
            return {"similarity_score": 0.0, "analysis": "Insufficient code samples"}
        
        # Simulated similarity analysis
        similarity_scores = []
        for i, e1 in enumerate(code_evidence):
            for e2 in code_evidence[i+1:]:
                # Calculate hash-based similarity (simplified)
                hash_diff = sum(
                    a != b for a, b in 
                    zip(e1.content_hash[:16], e2.content_hash[:16])
                ) / 16
                similarity = 1 - hash_diff
                similarity_scores.append(similarity)
        
        avg_similarity = sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0
        
        return {
            "similarity_score": round(avg_similarity, 3),
            "samples_analyzed": len(code_evidence),
            "potential_plagiarism": avg_similarity > 0.8,
            "analysis": "High similarity detected" if avg_similarity > 0.8 else "Distinct implementations"
        }
    
    def _assess_evidence(self, evidence_list: List[Evidence]) -> dict:
        """Assess credibility and weight of evidence"""
        assessment = {
            "total_evidence": len(evidence_list),
            "verified": 0,
            "by_type": {},
            "credibility_score": 0.0
        }
        
        type_weight = 0
        for evidence in evidence_list:
            # Count by type
            if evidence.evidence_type not in assessment["by_type"]:
                assessment["by_type"][evidence.evidence_type] = 0
            assessment["by_type"][evidence.evidence_type] += 1
            
            if evidence.verified:
                assessment["verified"] += 1
            
            # Calculate weighted credibility
            weight = self.weights.get(evidence.evidence_type, 0.05)
            type_weight += weight * (1.5 if evidence.verified else 1.0)
        
        if evidence_list:
            assessment["credibility_score"] = round(type_weight / len(evidence_list), 3)
        
        return assessment
    
    def _calculate_party_score(self, party: DisputeParty, evidence_list: List[Evidence]) -> float:
        """Calculate overall score for a party"""
        party_evidence = [e for e in evidence_list if e.submitted_by == party.wallet_address]
        
        if not party_evidence:
            return 0.0
        
        score = 0.0
        for evidence in party_evidence:
            base_weight = self.weights.get(evidence.evidence_type, 0.05)
            verified_bonus = 1.5 if evidence.verified else 1.0
            score += base_weight * verified_bonus * evidence.weight
        
        # Normalize
        return round(min(score * 10, 100), 1)
    
    def _generate_recommendation(self, analysis: dict, dispute: Dispute) -> dict:
        """Generate resolution recommendation"""
        party_scores = analysis["party_scores"]
        
        if not party_scores:
            return {
                "outcome": ResolutionOutcome.INSUFFICIENT_EVIDENCE.value,
                "reason": "No party scores available",
                "suggested_action": "Request additional evidence from all parties"
            }
        
        # Find highest scoring party
        sorted_parties = sorted(
            party_scores.items(),
            key=lambda x: x[1]['score'],
            reverse=True
        )
        
        top_party = sorted_parties[0]
        
        # Determine outcome based on scores
        if top_party[1]['score'] > 70:
            if top_party[1]['role'] == 'defendant':
                outcome = ResolutionOutcome.ORIGINAL_UPHELD
                reason = f"Original owner has strongest evidence (score: {top_party[1]['score']})"
            else:
                outcome = ResolutionOutcome.CLAIMANT_UPHELD
                reason = f"Claimant evidence is compelling (score: {top_party[1]['score']})"
        elif len(sorted_parties) > 1 and abs(sorted_parties[0][1]['score'] - sorted_parties[1][1]['score']) < 15:
            outcome = ResolutionOutcome.SHARED_OWNERSHIP
            reason = "Evidence suggests both parties have valid claims"
        else:
            outcome = ResolutionOutcome.REQUIRES_EXTERNAL_REVIEW
            reason = "Evidence is inconclusive - human review recommended"
        
        return {
            "outcome": outcome.value,
            "reason": reason,
            "winning_party": top_party[0] if outcome != ResolutionOutcome.SHARED_OWNERSHIP else None,
            "suggested_action": self._get_suggested_action(outcome),
            "suggested_split": self._calculate_suggested_split(sorted_parties, outcome)
        }
    
    def _get_suggested_action(self, outcome: ResolutionOutcome) -> str:
        """Get suggested action for outcome"""
        actions = {
            ResolutionOutcome.ORIGINAL_UPHELD: "Dismiss claim and maintain original ownership record",
            ResolutionOutcome.CLAIMANT_UPHELD: "Update ownership record to recognize claimant",
            ResolutionOutcome.SHARED_OWNERSHIP: "Create smart contract with agreed ownership split",
            ResolutionOutcome.PERCENTAGE_ADJUSTED: "Modify existing smart contract percentages",
            ResolutionOutcome.INSUFFICIENT_EVIDENCE: "Request additional evidence within 7 days",
            ResolutionOutcome.REQUIRES_EXTERNAL_REVIEW: "Schedule mediation session with neutral party"
        }
        return actions.get(outcome, "Review case manually")
    
    def _calculate_suggested_split(self, sorted_parties: list, outcome: ResolutionOutcome) -> dict:
        """Calculate suggested ownership split"""
        if outcome == ResolutionOutcome.SHARED_OWNERSHIP:
            if len(sorted_parties) >= 2:
                total_score = sum(p[1]['score'] for p in sorted_parties[:2])
                if total_score > 0:
                    return {
                        sorted_parties[0][1]['name']: round(sorted_parties[0][1]['score'] / total_score * 100),
                        sorted_parties[1][1]['name']: round(sorted_parties[1][1]['score'] / total_score * 100)
                    }
        return None
    
    def _calculate_confidence(self, analysis: dict) -> float:
        """Calculate confidence in the analysis"""
        factors = []
        
        # Evidence quantity
        evidence_factor = min(analysis["evidence_assessment"]["total_evidence"] / 10, 1.0)
        factors.append(evidence_factor * 0.3)
        
        # Verified evidence
        if analysis["evidence_assessment"]["total_evidence"] > 0:
            verified_ratio = analysis["evidence_assessment"]["verified"] / analysis["evidence_assessment"]["total_evidence"]
            factors.append(verified_ratio * 0.3)
        
        # Timeline clarity
        if analysis["timeline_analysis"]["timeline_clear"]:
            factors.append(0.2)
        
        # Party score difference
        scores = [p['score'] for p in analysis["party_scores"].values()]
        if len(scores) >= 2:
            score_diff = abs(scores[0] - scores[1]) / 100
            factors.append(score_diff * 0.2)
        
        return round(sum(factors) * 100, 1)


class DisputeResolutionSystem:
    """
    Complete dispute resolution system
    """
    
    def __init__(self):
        self.disputes = {}
        self.evidence = {}
        self.ai_engine = AIFairnessEngine()
        
    def file_dispute(self,
                     dispute_type: DisputeType,
                     original_tx_id: str,
                     project_title: str,
                     claimant: DisputeParty,
                     defendant: DisputeParty,
                     claim_summary: str) -> Dispute:
        """
        File a new dispute
        """
        dispute_id = hashlib.sha256(
            f"{original_tx_id}{claimant.wallet_address}{datetime.datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        claimant.role = "claimant"
        claimant.claim_summary = claim_summary
        defendant.role = "defendant"
        
        dispute = Dispute(
            id=dispute_id,
            type=dispute_type,
            status=DisputeStatus.PENDING,
            original_tx_id=original_tx_id,
            project_title=project_title,
            parties=[claimant, defendant],
            created_at=datetime.datetime.now().isoformat(),
            updated_at=datetime.datetime.now().isoformat(),
            timeline=[{
                "event": "dispute_filed",
                "timestamp": datetime.datetime.now().isoformat(),
                "actor": claimant.wallet_address,
                "details": claim_summary
            }]
        )
        
        self.disputes[dispute_id] = dispute
        print(f"\n📋 Dispute filed: {dispute_id}")
        print(f"   Type: {dispute_type.value}")
        print(f"   Project: {project_title}")
        print(f"   Claimant: {claimant.name}")
        print(f"   Defendant: {defendant.name}")
        
        return dispute
    
    def submit_evidence(self,
                        dispute_id: str,
                        submitted_by: str,
                        evidence_type: str,
                        description: str,
                        content: str) -> Evidence:
        """
        Submit evidence for a dispute
        """
        if dispute_id not in self.disputes:
            raise ValueError(f"Dispute {dispute_id} not found")
        
        dispute = self.disputes[dispute_id]
        
        evidence_id = hashlib.sha256(
            f"{dispute_id}{submitted_by}{content[:100]}".encode()
        ).hexdigest()[:12]
        
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # AI-assigned weight based on evidence type
        type_weights = {
            'blockchain': 1.0,
            'timestamp': 0.9,
            'code': 0.8,
            'document': 0.6,
            'commit_history': 0.7,
            'witness': 0.4
        }
        
        evidence = Evidence(
            id=evidence_id,
            dispute_id=dispute_id,
            submitted_by=submitted_by,
            evidence_type=evidence_type,
            description=description,
            content_hash=content_hash,
            submitted_at=datetime.datetime.now().isoformat(),
            verified=evidence_type == 'blockchain',  # Auto-verify blockchain evidence
            weight=type_weights.get(evidence_type, 0.5)
        )
        
        if dispute_id not in self.evidence:
            self.evidence[dispute_id] = []
        self.evidence[dispute_id].append(evidence)
        
        # Update party's evidence list
        for party in dispute.parties:
            if party.wallet_address == submitted_by:
                party.evidence_submitted.append(evidence_id)
                break
        
        # Update dispute status
        if dispute.status == DisputeStatus.PENDING:
            dispute.status = DisputeStatus.EVIDENCE_COLLECTION
        
        dispute.timeline.append({
            "event": "evidence_submitted",
            "timestamp": evidence.submitted_at,
            "actor": submitted_by,
            "details": f"Evidence type: {evidence_type}"
        })
        
        print(f"\n📎 Evidence submitted: {evidence_id}")
        print(f"   Type: {evidence_type}")
        print(f"   Weight: {evidence.weight}")
        print(f"   Verified: {'✅' if evidence.verified else '⏳'}")
        
        return evidence
    
    def trigger_ai_analysis(self, dispute_id: str) -> dict:
        """
        Trigger AI analysis for a dispute
        """
        if dispute_id not in self.disputes:
            raise ValueError(f"Dispute {dispute_id} not found")
        
        dispute = self.disputes[dispute_id]
        evidence_list = self.evidence.get(dispute_id, [])
        
        # Update status
        dispute.status = DisputeStatus.AI_ANALYSIS
        dispute.timeline.append({
            "event": "ai_analysis_started",
            "timestamp": datetime.datetime.now().isoformat(),
            "actor": "system",
            "details": "AI fairness engine analyzing dispute"
        })
        
        # Run AI analysis
        analysis = self.ai_engine.analyze_dispute(dispute, evidence_list)
        dispute.ai_analysis = analysis
        
        dispute.timeline.append({
            "event": "ai_analysis_completed",
            "timestamp": datetime.datetime.now().isoformat(),
            "actor": "system",
            "details": f"Recommendation: {analysis['recommendation']['outcome']}"
        })
        
        return analysis
    
    def resolve_dispute(self, dispute_id: str, accept_ai_recommendation: bool = True,
                        custom_resolution: dict = None) -> dict:
        """
        Resolve a dispute
        """
        if dispute_id not in self.disputes:
            raise ValueError(f"Dispute {dispute_id} not found")
        
        dispute = self.disputes[dispute_id]
        
        if accept_ai_recommendation and dispute.ai_analysis:
            resolution = {
                "outcome": dispute.ai_analysis["recommendation"]["outcome"],
                "reason": dispute.ai_analysis["recommendation"]["reason"],
                "decided_at": datetime.datetime.now().isoformat(),
                "method": "ai_recommendation",
                "confidence": dispute.ai_analysis["confidence"],
                "split": dispute.ai_analysis["recommendation"].get("suggested_split")
            }
        elif custom_resolution:
            resolution = {
                **custom_resolution,
                "decided_at": datetime.datetime.now().isoformat(),
                "method": "manual_resolution"
            }
        else:
            raise ValueError("No resolution specified")
        
        dispute.resolution = resolution
        dispute.status = DisputeStatus.RESOLVED
        dispute.updated_at = datetime.datetime.now().isoformat()
        
        dispute.timeline.append({
            "event": "dispute_resolved",
            "timestamp": resolution["decided_at"],
            "actor": "system",
            "details": f"Resolution: {resolution['outcome']}"
        })
        
        print(f"\n✅ Dispute {dispute_id[:8]} RESOLVED")
        print(f"   Outcome: {resolution['outcome']}")
        print(f"   Method: {resolution['method']}")
        print(f"   Confidence: {resolution.get('confidence', 'N/A')}%")
        
        return resolution
    
    def get_dispute_status(self, dispute_id: str) -> dict:
        """Get current status of a dispute"""
        if dispute_id not in self.disputes:
            return {"error": "Dispute not found"}
        
        dispute = self.disputes[dispute_id]
        return {
            "id": dispute.id,
            "type": dispute.type.value,
            "status": dispute.status.value,
            "project": dispute.project_title,
            "parties": [
                {"name": p.name, "role": p.role, "evidence_count": len(p.evidence_submitted)}
                for p in dispute.parties
            ],
            "created_at": dispute.created_at,
            "updated_at": dispute.updated_at,
            "timeline_events": len(dispute.timeline),
            "has_ai_analysis": dispute.ai_analysis is not None,
            "resolved": dispute.resolution is not None
        }


def demo_dispute_resolution():
    """Demo the dispute resolution system"""
    print("\n" + "="*70)
    print("⚖️  DISPUTE RESOLUTION SYSTEM DEMO")
    print("="*70)
    
    system = DisputeResolutionSystem()
    
    # Create parties
    claimant = DisputeParty(
        wallet_address="ALGO_CLAIMANT_123",
        name="Charlie Brown",
        role="claimant"
    )
    
    defendant = DisputeParty(
        wallet_address="ALGO_DEFENDANT_456",
        name="Alice Johnson",
        role="defendant"
    )
    
    # File dispute
    print("\n📋 STEP 1: Filing Dispute")
    print("-" * 50)
    
    dispute = system.file_dispute(
        dispute_type=DisputeType.OWNERSHIP_CLAIM,
        original_tx_id="ABCD1234EFGH5678IJKL",
        project_title="AI-Powered Code Analysis System",
        claimant=claimant,
        defendant=defendant,
        claim_summary="I developed the core algorithm before Alice's registration"
    )
    
    # Submit evidence
    print("\n📎 STEP 2: Submitting Evidence")
    print("-" * 50)
    
    # Claimant evidence
    system.submit_evidence(
        dispute_id=dispute.id,
        submitted_by=claimant.wallet_address,
        evidence_type="code",
        description="Original code from my local repository",
        content="def analyze_code(text): # My implementation from Jan 2026..."
    )
    
    system.submit_evidence(
        dispute_id=dispute.id,
        submitted_by=claimant.wallet_address,
        evidence_type="timestamp",
        description="Git commit from January 2026",
        content="commit abc123 - Initial implementation - Jan 15, 2026"
    )
    
    # Defendant evidence
    system.submit_evidence(
        dispute_id=dispute.id,
        submitted_by=defendant.wallet_address,
        evidence_type="blockchain",
        description="BrainBlock registration transaction",
        content="Transaction ABCD1234 - Block 35000000 - Feb 1, 2026"
    )
    
    system.submit_evidence(
        dispute_id=dispute.id,
        submitted_by=defendant.wallet_address,
        evidence_type="document",
        description="Project documentation",
        content="BrainBlock IP Registration Certificate..."
    )
    
    # Trigger AI analysis
    print("\n🤖 STEP 3: AI Analysis")
    print("-" * 50)
    
    analysis = system.trigger_ai_analysis(dispute.id)
    
    print(f"\n📊 Analysis Results:")
    print(f"   Confidence: {analysis['confidence']}%")
    print(f"   Timeline Analysis: {analysis['timeline_analysis']['total_timestamps']} timestamps analyzed")
    print(f"   Evidence Assessment: {analysis['evidence_assessment']['total_evidence']} pieces of evidence")
    
    print(f"\n   Party Scores:")
    for wallet, data in analysis['party_scores'].items():
        print(f"   • {data['name']} ({data['role']}): {data['score']} points")
    
    print(f"\n   Recommendation: {analysis['recommendation']['outcome']}")
    print(f"   Reason: {analysis['recommendation']['reason']}")
    
    # Resolve dispute
    print("\n✅ STEP 4: Resolution")
    print("-" * 50)
    
    resolution = system.resolve_dispute(dispute.id, accept_ai_recommendation=True)
    
    # Show final status
    print("\n📋 Final Status:")
    status = system.get_dispute_status(dispute.id)
    for key, value in status.items():
        if key != 'parties':
            print(f"   {key}: {value}")
    
    print("\n" + "="*70)
    print("✅ DISPUTE RESOLUTION DEMO COMPLETE")
    print("="*70)


if __name__ == "__main__":
    demo_dispute_resolution()
