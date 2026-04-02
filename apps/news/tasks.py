from celery import shared_task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

# bind=True allows us to use self.retry
@shared_task(bind=True, max_retries=3)
def send_async_email(self, user_email, subject, body):
    """
    Sends an email in the background via the ECS worker.
    """
    logger.info(f"Worker preparing to send email to {user_email}...")

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email='noreply@rightbanker.com', # Update to your verified domain
            recipient_list=[user_email],
            fail_silently=False, # We want it to fail so Celery can catch and retry
        )

        logger.info(f"Successfully delivered email to {user_email}!")
        return {"status": "success", "recipient": user_email}

    except Exception as exc:
        logger.warning(f"Email delivery failed. Retrying... Attempt {self.request.retries + 1}")
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
