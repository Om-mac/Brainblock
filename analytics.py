"""
Analytics & Dashboard Module  
Real-time metrics and insights for BrainBlock
"""

import datetime
import random
from typing import List, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Metric:
    """A single metric data point"""
    name: str
    value: float
    unit: str
    timestamp: str
    tags: dict = None


@dataclass
class TimeSeriesPoint:
    """Time series data point"""
    timestamp: str
    value: float


class AnalyticsEngine:
    """
    Analytics engine for tracking platform metrics
    
    Integrates with:
    - AWS CloudWatch (infrastructure metrics)
    - Mixpanel/Amplitude (product analytics)
    - Custom dashboards
    """
    
    def __init__(self):
        self._events = []
        self._metrics = defaultdict(list)
        
    def track_event(self, event_name: str, properties: dict = None,
                   user_id: Optional[str] = None) -> None:
        """Track an analytics event"""
        event = {
            "event": event_name,
            "properties": properties or {},
            "user_id": user_id,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self._events.append(event)
        
    def record_metric(self, name: str, value: float, 
                     unit: str = "count", tags: dict = None) -> None:
        """Record a metric value"""
        metric = Metric(
            name=name,
            value=value,
            unit=unit,
            timestamp=datetime.datetime.now().isoformat(),
            tags=tags
        )
        self._metrics[name].append(metric)
        
    def get_time_series(self, metric_name: str, 
                       period: str = "24h") -> List[TimeSeriesPoint]:
        """Get time series data for a metric"""
        return self._metrics.get(metric_name, [])


class DashboardMetrics:
    """
    Dashboard metrics provider
    Generates real-time statistics for the admin dashboard
    """
    
    def __init__(self):
        self.analytics = AnalyticsEngine()
        
    def get_overview(self) -> dict:
        """Get platform overview metrics"""
        # Simulated metrics for demo
        return {
            "total_submissions": 15234,
            "submissions_today": 89,
            "submissions_change": "+12%",
            "total_users": 8456,
            "active_users_today": 342,
            "users_change": "+8%",
            "total_groups": 1876,
            "blockchain_transactions": 18459,
            "total_protected_value": "$2.4M (estimated)",
            "uptime": "99.97%"
        }
    
    def get_submission_stats(self) -> dict:
        """Get submission statistics"""
        return {
            "by_type": {
                "code": 8234,
                "documentation": 3421,
                "design": 1876,
                "mixed": 1703
            },
            "by_originality": {
                "highly_original": 12456,
                "original": 2134,
                "needs_review": 432,
                "rejected": 212
            },
            "by_complexity": {
                "high": 4532,
                "medium": 7823,
                "low": 2879
            },
            "avg_processing_time": "2.3 seconds",
            "success_rate": "98.6%"
        }
    
    def get_user_stats(self) -> dict:
        """Get user statistics"""
        return {
            "by_type": {
                "students": 6234,
                "faculty": 876,
                "professionals": 1346
            },
            "by_region": {
                "north_america": 3245,
                "europe": 2876,
                "asia": 1987,
                "other": 348
            },
            "top_universities": [
                {"name": "MIT", "users": 234, "submissions": 567},
                {"name": "Stanford", "users": 198, "submissions": 432},
                {"name": "Berkeley", "users": 176, "submissions": 398},
                {"name": "CMU", "users": 154, "submissions": 321},
                {"name": "Georgia Tech", "users": 143, "submissions": 287}
            ],
            "wallet_connections": {
                "pera": 3245,
                "myalgo": 2876,
                "algosigner": 1987,
                "other": 348
            }
        }
    
    def get_blockchain_stats(self) -> dict:
        """Get blockchain statistics"""
        return {
            "network": "Algorand Mainnet",
            "total_transactions": 18459,
            "transactions_today": 156,
            "avg_confirmation_time": "4.2 seconds",
            "total_fees_paid": "18.459 ALGO",
            "smart_contracts_deployed": 1876,
            "verification_requests": 4532,
            "successful_verifications": 4498
        }
    
    def get_hourly_submissions(self) -> List[dict]:
        """Get hourly submission data for chart"""
        hours = []
        base = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        
        for i in range(24):
            hour = base - datetime.timedelta(hours=23-i)
            hours.append({
                "hour": hour.strftime("%H:00"),
                "submissions": random.randint(2, 15),
                "verifications": random.randint(5, 25)
            })
        
        return hours
    
    def get_daily_submissions(self, days: int = 30) -> List[dict]:
        """Get daily submission data for chart"""
        data = []
        base = datetime.datetime.now().date()
        
        for i in range(days):
            day = base - datetime.timedelta(days=days-1-i)
            data.append({
                "date": day.isoformat(),
                "submissions": random.randint(50, 150),
                "users": random.randint(100, 400)
            })
        
        return data


class LeaderboardService:
    """
    Leaderboard and rankings
    """
    
    def get_top_contributors(self, limit: int = 10) -> List[dict]:
        """Get top contributors by submissions"""
        return [
            {"rank": i+1, "username": f"user_{i}", "submissions": 100-i*8, 
             "originality_avg": round(0.95 - i*0.02, 2)}
            for i in range(limit)
        ]
    
    def get_top_universities(self, limit: int = 10) -> List[dict]:
        """Get top universities by activity"""
        universities = [
            "MIT", "Stanford", "Berkeley", "CMU", "Georgia Tech",
            "Harvard", "Caltech", "Princeton", "Cornell", "Yale"
        ]
        return [
            {"rank": i+1, "name": universities[i], 
             "users": 200-i*15, "submissions": 500-i*40}
            for i in range(min(limit, len(universities)))
        ]
    
    def get_trending_projects(self, limit: int = 10) -> List[dict]:
        """Get trending projects by verification requests"""
        return [
            {"rank": i+1, "title": f"Innovative Project {i+1}", 
             "author": f"user_{i}", "verifications": 50-i*4,
             "created": (datetime.datetime.now() - datetime.timedelta(days=i)).isoformat()}
            for i in range(limit)
        ]


class ReportGenerator:
    """
    Generate analytics reports
    """
    
    def __init__(self):
        self.dashboard = DashboardMetrics()
        self.leaderboard = LeaderboardService()
        
    def generate_weekly_report(self) -> dict:
        """Generate weekly platform report"""
        overview = self.dashboard.get_overview()
        submissions = self.dashboard.get_submission_stats()
        
        return {
            "report_type": "weekly",
            "generated_at": datetime.datetime.now().isoformat(),
            "period": {
                "start": (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat(),
                "end": datetime.datetime.now().isoformat()
            },
            "highlights": {
                "total_submissions": overview["submissions_today"] * 7,
                "new_users": int(overview["active_users_today"] * 0.3 * 7),
                "success_rate": submissions["success_rate"],
                "top_project": self.leaderboard.get_trending_projects(1)[0]
            },
            "charts_data": {
                "daily_submissions": self.dashboard.get_daily_submissions(7),
                "top_contributors": self.leaderboard.get_top_contributors(5)
            }
        }
    
    def generate_user_report(self, user_id: str) -> dict:
        """Generate individual user report"""
        return {
            "user_id": user_id,
            "generated_at": datetime.datetime.now().isoformat(),
            "summary": {
                "total_submissions": random.randint(5, 50),
                "group_projects": random.randint(1, 10),
                "avg_originality": round(random.uniform(0.85, 0.99), 2),
                "verifications_received": random.randint(10, 100)
            },
            "recent_activity": [
                {
                    "type": "submission",
                    "title": "Project Alpha",
                    "date": datetime.datetime.now().isoformat()
                }
            ],
            "achievements": [
                {"name": "First Submission", "earned": True},
                {"name": "10 Projects Protected", "earned": True},
                {"name": "Top Contributor", "earned": False}
            ]
        }


class InsightsEngine:
    """
    AI-powered insights and recommendations
    """
    
    def get_user_insights(self, user_id: str) -> List[dict]:
        """Get personalized insights for a user"""
        return [
            {
                "type": "tip",
                "title": "Improve Originality Score",
                "message": "Adding more technical details to your submissions can increase originality scores by up to 15%",
                "action": "Learn More"
            },
            {
                "type": "achievement",
                "title": "Almost There!",
                "message": "Submit 2 more projects to earn the 'Prolific Innovator' badge",
                "progress": 80
            },
            {
                "type": "recommendation",
                "title": "Consider Group Projects",
                "message": "Students who collaborate have 23% higher success in hackathons",
                "action": "Start a Group"
            }
        ]
    
    def get_platform_insights(self) -> List[dict]:
        """Get platform-wide insights for admins"""
        return [
            {
                "type": "trend",
                "title": "Rising Interest in AI",
                "message": "AI/ML related submissions increased 45% this month",
                "change": "+45%"
            },
            {
                "type": "alert",
                "title": "Peak Hours Detected",
                "message": "Submissions peak between 2-4 PM EST. Consider scaling resources.",
                "severity": "info"
            },
            {
                "type": "opportunity",
                "title": "University Partnership",
                "message": "5 new universities showed interest this week",
                "action": "View Details"
            }
        ]
