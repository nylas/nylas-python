from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class Calendar:
    id: str
    grant_id: str
    name: str
    timezone: str
    read_only: bool
    is_owned_by_user: bool
    description: Optional[str]
    location: Optional[str]
    hex_color: Optional[str]
    hex_foreground_color: Optional[str]
    is_primary: Optional[bool]
    metadata: Optional[Dict[str, Any]]
    object: str = "calendar"
