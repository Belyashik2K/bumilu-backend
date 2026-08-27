from app.modules.auth.application.interfaces.email_dispatcher import IEmailDispatcher
from app.modules.auth.infrastructure.queue.tasks.send_email import send_email_task


class TaskiqEmailDispatcher(IEmailDispatcher):
    async def dispatch(self, *, to: str, subject: str, body: str) -> None:
        # `sender` is injected by dishka's `@inject` decorator at runtime and
        # must not be passed here; mypy doesn't understand that rewiring.
        await send_email_task.kiq(  # type: ignore[call-overload]
            to=to, subject=subject, body=body
        )
