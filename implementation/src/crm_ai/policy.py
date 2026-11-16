from enum import Enum

class Action(str, Enum):
    READ_CONTACT = "read_contact"
    DRAFT_MESSAGE = "draft_message"
    SEND_MESSAGE = "send_message"
    UPDATE_CONTACT = "update_contact"
    DELETE_CONTACT = "delete_contact"

HIGH_RISK = {Action.SEND_MESSAGE, Action.UPDATE_CONTACT, Action.DELETE_CONTACT}

def authorize_action(action: Action, approved: bool = False) -> bool:
    # Fail closed: high-impact actions are denied unless approval is explicitly present.
    if action in HIGH_RISK:
        return approved
    return True
