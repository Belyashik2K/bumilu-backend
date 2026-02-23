from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestEmailCodeAtLoginInputDTO:
    email: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestEmailCodeAtLoginOutputDTO: ...
