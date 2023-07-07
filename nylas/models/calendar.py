from dataclasses import dataclass
from typing import Dict, Any, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Calendar:
    id: str
    grant_id: str
    name: str
    timezone: str
    read_only: bool
    is_owned_by_user: bool
    object: str = "calendar"
    description: Optional[str] = None
    location: Optional[str] = None
    hex_color: Optional[str] = None
    hex_foreground_color: Optional[str] = None
    is_primary: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
