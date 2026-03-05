from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class ProcessPendingChatsInputDTO: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class ProcessPendingChatsOutputDTO: ...
