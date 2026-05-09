import ssl
import smtplib
import certifi
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend


class CertifiEmailBackend(EmailBackend):
    """SMTP backend with certifi CA bundle. Disables cert verification in DEBUG mode
    to handle corporate proxies or antivirus SSL interception on Windows."""

    def _build_ssl_context(self):
        if getattr(settings, 'DEBUG', False):
            # Dev only: skip verification to avoid proxy/AV SSL interception issues
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        else:
            context = ssl.create_default_context(cafile=certifi.where())
        return context

    def open(self):
        if self.connection:
            return False

        connection_params = {}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout

        try:
            context = self._build_ssl_context()

            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(
                    self.host, self.port, context=context, **connection_params
                )
            else:
                self.connection = smtplib.SMTP(self.host, self.port, **connection_params)
                self.connection.ehlo()
                if self.use_tls:
                    self.connection.starttls(context=context)
                    self.connection.ehlo()

            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except OSError:
            if not self.fail_silently:
                raise
