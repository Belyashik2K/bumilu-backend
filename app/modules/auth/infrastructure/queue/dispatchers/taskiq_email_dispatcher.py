from app.modules.auth.application.interfaces.email_dispatcher import IEmailDispatcher
from app.modules.auth.infrastructure.queue.tasks.send_email import send_email_task


class TaskiqEmailDispatcher(IEmailDispatcher):
    async def dispatch(self, *, to: str, subject: str, body: str) -> None:
        await send_email_task.kiq(to=to, subject=subject, body=body)
