import logging
import OpenSSL
import pem
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import common

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IInstaller)
@zope.interface.provider(interfaces.IPluginFactory)
class PKCS12Installer(common.Plugin):
    """PKCS12 installer"""

    description = "PKCS12 installer plugin"

    @classmethod
    def add_parser_arguments(cls, add):
        add("path", help="PKCS12 path")
        add("pass", help="PKCS12 password")

    def prepare(self):
        self.config_test()

    @staticmethod
    def more_info():
        pass

    def get_all_names(self):
        return []

    def deploy_cert(self, domain, cert_path, key_path,
                    chain_path=None, fullchain_path=None):
        pkcs12 = OpenSSL.crypto.PKCS12()
        pkcs12.set_friendlyname(domain.encode("utf-8"))

        with open(cert_path, "rb") as f:
            cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())
        pkcs12.set_certificate(cert)

        with open(key_path, "rb") as f:
            key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, f.read())
        pkcs12.set_privatekey(key)

        if chain_path:
            chain = pem.parse_file(chain_path)
            ca_certs = [
                OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c.as_bytes())
                for c in chain
            ]
            pkcs12.set_ca_certificates(ca_certs)

        with open(self.conf("path"), "wb") as f:
            f.write(pkcs12.export(self.conf("pass")))

    def enhance(self, domain, enchancement, options=None):
        pass

    def supported_enhancements(self):
        return []

    def save(self, title=None, temporary=False):
        pass

    def rollback_checkpoints(self, rollback=1):
        pass

    def recovery_routine(self):
        pass

    def view_config_changes(self):
        pass

    def config_test(self):
        if self.conf("path") is None:
            raise errors.MisconfigurationError("PKCS12 path is not set")

    def restart(self):
        pass
