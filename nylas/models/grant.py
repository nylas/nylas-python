from dataclasses import dataclass
from typing import List, Any, Dict, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Grant:
    id: str
    provider: str
    scope: List[str]
    created_at: int
    grant_status: Optional[str] = None
    email: Optional[str] = None
    user_agent: Optional[str] = None
    ip: Optional[str] = None
    state: Optional[str] = None
    updated_at: Optional[int] = None
    provider_user_id: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
