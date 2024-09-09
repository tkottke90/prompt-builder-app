import datetime
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Neo4JTimestampModel():
  createdAt: datetime.datetime = field(default_factory=datetime.datetime.now)
  updatedAt: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class Neo4jNodeMetadata:
  id: int
  labels: Optional[List[str]]
