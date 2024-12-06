from typing import Optional, List

class Manager:
    def __init__(self, id: str, avatar_url: str, first_name: str, last_name: str, full_name: str):
        self.id = id
        self.avatar_url = avatar_url
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name


class Customer:
    def __init__(self, full_name: str, phone_number: str, managers: List[Manager]):
        self.full_name = full_name
        self.phone_number = phone_number
        self.managers = managers


class Chat:
    def __init__(self, id: str, channel_id: str, last_message_at: str, last_message_text: str,
                 status: str, is_unread: bool, is_closed: bool, sending_blocked_reason: Optional[str], customer: Customer, tags: List[str]):
        self.id = id
        self.channel_id = channel_id
        self.last_message_at = last_message_at
        self.last_message_text = last_message_text
        self.status = status
        self.is_unread = is_unread
        self.is_closed = is_closed
        self.sending_blocked_reason = sending_blocked_reason
        self.customer = customer
        self.tags = tags


class Message:
    def __init__(self, id: str, created_at: str, updated_at: str, chat_id: str, system_type: str,
                 replied_to: Optional[str], sent_by: dict, status: dict, message_id: str,
                 message_type: str, message_preview: str, message_payload: dict):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.chat_id = chat_id
        self.system_type = system_type
        self.replied_to = replied_to
        self.sent_by = sent_by
        self.status = status
        self.message_id = message_id
        self.message_type = message_type
        self.message_preview = message_preview
        self.message_payload = message_payload


class Pub:
    def __init__(self, data: dict):
        self.data = data
        self.event_type = data.get("event_type")
        self.chat_id = data.get("chat_id")
        self.message_id = data.get("message_id")
        self.status = data.get("status")
        self.chat = Chat(**data["chat"])
        self.message = Message(**data["message"])


class Push:
    def __init__(self, channel: str, pub: Pub):
        self.channel = channel
        self.pub = pub


class WebSocketData:
    def __init__(self, push: dict):
        self.push = Push(push["channel"], Pub(push["pub"]["data"]))
