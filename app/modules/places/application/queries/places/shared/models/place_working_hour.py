from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceWorkingHourReadModel:
    start: time
    end: time
