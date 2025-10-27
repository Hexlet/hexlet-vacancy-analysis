import logging
import socket
import time
from smtplib import (
    SMTPAuthenticationError,
    SMTPConnectError,
    SMTPException,
    SMTPServerDisconnected,
)

from django.core.mail import send_mail

from ..exceptions import SendEmailError

logger = logging.getLogger(__name__)

SUBJECT_MAIL = "Confirm registration"
SENDER_MAIL = "noreply@example.com"
MAX_RETRIES = 3
RETRY_DELAY = 2
SEND_SUCCESSFULLY_MSG = "Email sent successfully"
SEND_FAILED_MSG = "Connection error, server unavailable"
SMTP_AUTHENTICATION_ERROR_MSG = "SMTP authorization error"
SMTP_ERROR_MSG = SMTP_AUTHENTICATION_ERROR_MSG = "SMTP error"
UNEXPECTED_ERROR_MSG = "An unexpected error occurred while sending the"


def safe_send_mail(message, recipient, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
    attempt = 1
    while attempt <= max_retries:
        try:
            send_mail(
                subject=SUBJECT_MAIL,
                message=message,
                from_email=SENDER_MAIL,
                recipient_list=recipient,
                fail_silently=False,
            )
            status_message = SEND_SUCCESSFULLY_MSG
            logger.info(f"{status_message}, {attempt} attempt)")
            return

        except SMTPAuthenticationError:
            status_message = SMTP_AUTHENTICATION_ERROR_MSG
            raise SendEmailError(message=status_message, code=500)

        except (
            SMTPConnectError,
            SMTPServerDisconnected,
            socket.timeout,
            socket.gaierror,
        ) as e:
            logger.warning(" (%s): %s (попытка %s)", recipient, str(e), attempt)

            if attempt == max_retries:
                status_message = SEND_FAILED_MSG
                logger.error(
                    f"{status_message} \
                    ({recipient}) \
                    after {max_retries} attempts"
                )
                raise SendEmailError(message=status_message, code=500)

            time.sleep(retry_delay)
            attempt += 1
            continue

        except SMTPException:
            status_message = SMTP_ERROR_MSG
            raise SendEmailError(message=status_message, code=500)

        except Exception:
            status_message = UNEXPECTED_ERROR_MSG
            raise SendEmailError(message=status_message, code=500)
