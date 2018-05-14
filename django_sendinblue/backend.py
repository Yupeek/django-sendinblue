import sib_api_v3_sdk

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.base import BaseEmailBackend


class SendinblueBackend(BaseEmailBackend):
    """
    Sendinblue email backend using sib-api-v3-sdk for django
    """

    def __init__(self, *args, **kwargs):
        super(SendinblueBackend, self).__init__(*args, **kwargs)

        try:
            api_key = settings.SENDINBLUE_API_KEY
        except AttributeError:
            raise ImproperlyConfigured('Please set Send in blue API key in settings.')

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        self.smtp_api = sib_api_v3_sdk.SMTPApi(sib_api_v3_sdk.ApiClient(configuration))

    def _get_sib_attachments(self, message):
        sib_attachments = []
        for attachment in message.attachments():
            sib_attachments.append(sib_api_v3_sdk.SendEmailAttachment(
                content=attachment[1],
                name=attachment[0]
            ))
        return sib_attachments

    def _get_sib_attributes(self, message, to_email=None):
        attributes = message.global_merge_vars.copy()
        if not message.use_template_from:
            attributes.update({'SUBJECT': message.subject})

        try:
            attributes.update(message.merge_vars.get(to_email, {}))
        except AttributeError:
            pass  # No specific merge tag for this recipient

        return attributes

    def _send(self, message):
        if not message.recipients():
            return False

        sib_attachments = self._get_sib_attachments(message)
        for to_email in message.to:
            recipient_attributes = self._get_sib_attributes(message, to_email=to_email)
            sib_message = sib_api_v3_sdk.SendEmail(
                email_to=to_email,
                email_cc=message.cc,
                email_bcc=message.bcc,
                headers=message.extra_headers,
                attributes=recipient_attributes,
                attachment=sib_attachments,
            )
            # TODO: need to change that template_name, its actually id for sib :@
            self.smtp_api.send_template(message.template_name, sib_message)
            # TODO: parse response and error management
        return True

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        num_sent = 0
        for message in email_messages:
            if self._send(message):
                num_sent += 1
        return num_sent
