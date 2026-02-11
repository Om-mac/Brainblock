"""
Notification & Email Service
Multi-channel notifications for BrainBlock events
"""

import datetime
import hashlib
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class NotificationType(Enum):
    """Types of notifications"""
    SUBMISSION_CONFIRMED = "submission_confirmed"
    BLOCKCHAIN_REGISTERED = "blockchain_registered"
    GROUP_INVITE = "group_invite"
    CONTRIBUTION_ADDED = "contribution_added"
    OWNERSHIP_APPROVED = "ownership_approved"
    DISPUTE_ALERT = "dispute_alert"
    VERIFICATION_REQUEST = "verification_request"


@dataclass
class Notification:
    """Notification object"""
    id: str
    type: NotificationType
    title: str
    message: str
    recipient: str
    channel: str
    sent_at: str
    read: bool = False
    data: dict = None


class EmailService:
    """
    AWS SES Email Service
    
    Use Cases:
    - Submission confirmations
    - Ownership certificates
    - Team invitations
    - Dispute alerts
    """
    
    TEMPLATES = {
        "submission_confirmed": {
            "subject": "🎉 Your innovation is now protected - BrainBlock",
            "body": """
Hi {name},

Great news! Your project "{title}" has been successfully registered on the blockchain.

📋 Details:
- Transaction ID: {tx_id}
- Block: {block}
- Timestamp: {timestamp}

🔗 View your proof: {explorer_url}

Share this link with anyone to prove your ownership!

Best,
The BrainBlock Team
            """
        },
        "group_invite": {
            "subject": "You've been invited to a BrainBlock group project",
            "body": """
Hi {name},

{inviter} has invited you to join the project "{title}" on BrainBlock.

Your proposed contribution: {contribution_type}
Suggested ownership: {ownership}%

Click here to accept: {accept_url}

Best,
The BrainBlock Team
            """
        },
        "ownership_certificate": {
            "subject": "📜 Your BrainBlock Ownership Certificate",
            "body": """
Hi {name},

This is your official ownership certificate for "{title}".

Certificate Details:
- Owner: {name}
- Ownership: {ownership}%
- Blockchain Hash: {hash}
- Verified: ✅

This certificate is permanently recorded on the Algorand blockchain.

Best,
The BrainBlock Team
            """
        }
    }
    
    def __init__(self, sender_email: str = "noreply@brainblock.io"):
        self.sender = sender_email
        self._sent_emails = []
        
    def send_email(self, to: str, template: str, data: dict) -> dict:
        """Send templated email"""
        if template not in self.TEMPLATES:
            return {"error": f"Unknown template: {template}"}
        
        tmpl = self.TEMPLATES[template]
        subject = tmpl["subject"].format(**data) if data else tmpl["subject"]
        body = tmpl["body"].format(**data) if data else tmpl["body"]
        
        email = {
            "id": hashlib.md5(f"{to}{datetime.datetime.now()}".encode()).hexdigest()[:16],
            "to": to,
            "from": self.sender,
            "subject": subject,
            "body": body,
            "sent_at": datetime.datetime.now().isoformat(),
            "status": "sent"
        }
        
        self._sent_emails.append(email)
        
        return {
            "success": True,
            "message_id": email["id"],
            "to": to,
            "subject": subject
        }
    
    def send_certificate(self, to: str, project_data: dict) -> dict:
        """Send ownership certificate email"""
        return self.send_email(to, "ownership_certificate", project_data)


class PushNotificationService:
    """
    Push Notifications via Firebase Cloud Messaging (FCM)
    """
    
    def __init__(self):
        self._subscriptions = {}
        self._notifications = []
        
    def subscribe(self, user_id: str, device_token: str) -> dict:
        """Subscribe device to push notifications"""
        if user_id not in self._subscriptions:
            self._subscriptions[user_id] = []
        self._subscriptions[user_id].append(device_token)
        
        return {"subscribed": True, "user_id": user_id}
    
    def send_push(self, user_id: str, title: str, body: str, 
                  data: Optional[dict] = None) -> dict:
        """Send push notification"""
        if user_id not in self._subscriptions:
            return {"error": "User not subscribed"}
        
        notification = {
            "id": hashlib.md5(f"{user_id}{datetime.datetime.now()}".encode()).hexdigest()[:16],
            "user_id": user_id,
            "title": title,
            "body": body,
            "data": data,
            "sent_at": datetime.datetime.now().isoformat()
        }
        
        self._notifications.append(notification)
        
        return {
            "success": True,
            "notification_id": notification["id"],
            "devices_reached": len(self._subscriptions[user_id])
        }


class WebhookService:
    """
    Webhook notifications for integrations
    """
    
    def __init__(self):
        self._webhooks = {}
        self._deliveries = []
        
    def register_webhook(self, user_id: str, url: str, 
                        events: List[str]) -> dict:
        """Register a webhook endpoint"""
        webhook_id = hashlib.md5(f"{user_id}{url}".encode()).hexdigest()[:16]
        
        self._webhooks[webhook_id] = {
            "id": webhook_id,
            "user_id": user_id,
            "url": url,
            "events": events,
            "secret": hashlib.sha256(webhook_id.encode()).hexdigest()[:32],
            "created_at": datetime.datetime.now().isoformat(),
            "active": True
        }
        
        return {
            "webhook_id": webhook_id,
            "secret": self._webhooks[webhook_id]["secret"],
            "events": events
        }
    
    def trigger_webhook(self, event: str, payload: dict) -> List[dict]:
        """Trigger webhooks for an event"""
        results = []
        
        for webhook in self._webhooks.values():
            if webhook["active"] and event in webhook["events"]:
                # Simulate webhook delivery
                delivery = {
                    "webhook_id": webhook["id"],
                    "event": event,
                    "payload": payload,
                    "delivered_at": datetime.datetime.now().isoformat(),
                    "status": "delivered",
                    "response_code": 200
                }
                self._deliveries.append(delivery)
                results.append(delivery)
        
        return results


class SlackIntegration:
    """
    Slack notifications for teams
    """
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        
    def send_message(self, channel: str, text: str, 
                    blocks: Optional[List[dict]] = None) -> dict:
        """Send Slack message"""
        return {
            "success": True,
            "channel": channel,
            "ts": f"{datetime.datetime.now().timestamp()}"
        }
    
    def send_submission_alert(self, project_title: str, 
                              tx_id: str, explorer_url: str) -> dict:
        """Send submission confirmation to Slack"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🧠 BrainBlock: New Submission Protected"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Project:*\n{project_title}"},
                    {"type": "mrkdwn", "text": f"*TX ID:*\n{tx_id[:16]}..."}
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View on Explorer"},
                        "url": explorer_url
                    }
                ]
            }
        ]
        
        return self.send_message("#brainblock-alerts", "", blocks)


class DiscordIntegration:
    """
    Discord notifications for communities
    """
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        
    def send_embed(self, title: str, description: str, 
                  color: int = 0x00ff00, fields: List[dict] = None) -> dict:
        """Send Discord embed message"""
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "fields": fields or [],
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "embed": embed
        }
    
    def send_submission_alert(self, project_title: str, 
                              author: str, explorer_url: str) -> dict:
        """Send submission confirmation to Discord"""
        return self.send_embed(
            title="🧠 New Innovation Protected!",
            description=f"**{project_title}** by {author}",
            color=0x6366f1,
            fields=[
                {"name": "Status", "value": "✅ Verified", "inline": True},
                {"name": "Blockchain", "value": "[View Proof](" + explorer_url + ")", "inline": True}
            ]
        )


class NotificationHub:
    """
    Unified notification management
    """
    
    def __init__(self):
        self.email = EmailService()
        self.push = PushNotificationService()
        self.webhook = WebhookService()
        self.slack = SlackIntegration()
        self.discord = DiscordIntegration()
        
    def notify_submission_confirmed(self, user_data: dict, 
                                     submission_data: dict) -> dict:
        """Send submission confirmation across all channels"""
        results = {}
        
        # Email notification
        if user_data.get("email"):
            results["email"] = self.email.send_email(
                user_data["email"],
                "submission_confirmed",
                {
                    "name": user_data.get("name", "User"),
                    "title": submission_data.get("title", "Untitled"),
                    "tx_id": submission_data.get("tx_id", ""),
                    "block": submission_data.get("block", ""),
                    "timestamp": submission_data.get("timestamp", ""),
                    "explorer_url": submission_data.get("explorer_url", "")
                }
            )
        
        # Push notification
        if user_data.get("user_id"):
            results["push"] = self.push.send_push(
                user_data["user_id"],
                "Innovation Protected! 🎉",
                f"Your project '{submission_data.get('title')}' is now on the blockchain"
            )
        
        # Webhook
        results["webhooks"] = self.webhook.trigger_webhook(
            "submission.confirmed",
            submission_data
        )
        
        return results
    
    def notify_group_invite(self, inviter: str, invitee_email: str,
                           project_data: dict) -> dict:
        """Send group project invitation"""
        return self.email.send_email(
            invitee_email,
            "group_invite",
            {
                "name": invitee_email.split("@")[0],
                "inviter": inviter,
                "title": project_data.get("title", ""),
                "contribution_type": project_data.get("contribution_type", ""),
                "ownership": project_data.get("ownership", 0),
                "accept_url": f"https://brainblock.io/invite/{project_data.get('invite_id', '')}"
            }
        )
