from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.core.infrastructure.queue.broker import broker
from app.modules.auth.application.interfaces.email_sender import IEmailSender


@broker.task
@inject(patch_module=True)
async def send_email_task(
    sender: FromDishka[IEmailSender], to: str, subject: str, body: str
) -> None:
    await sender.send(to=to, subject=subject, body=body)
