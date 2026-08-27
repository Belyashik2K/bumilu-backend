from typing import Any

from starlette.datastructures import State
from starlette.requests import Request

from app.modules.auth.shared.context import Principal


class CustomState(State):
    def __init__(self, state: dict[str, Any] | None = None):
        super().__init__(state)
        self.principal: Principal | None = None


class CustomRequest(Request):
    @property
    def state(self) -> CustomState:
        if not hasattr(self, "_state"):
            # Ensure 'state' has an empty dict if it's not already populated.
            self.scope.setdefault("state", {})
            # Create a state instance with a reference to the dict in which it should
            # store info
            self._state: CustomState = CustomState(self.scope["state"])
        return self._state
