import os
import subprocess
import yaml
import requests

IP_SERVICE_API_URL = 'https://api.ipify.org'


class Configuration(object):

    DEFAULT_PORT = 8443
    LISTEN_ADDRESS = '0.0.0.0'
    SSL_CERT = 'webhook_cert.pem'
    SSL_KEY = 'webhook_pkey.pem'

    def __init__(self):
        self.ip_addr = os.environ.get('SERVER_ADDR',
                                      Configuration.get_external_ip())
        self.port = os.environ.get('SERVER_PORT',
                                   Configuration.DEFAULT_PORT)
        self.listen = os.environ.get('LISTEN_ADDR',
                                     Configuration.LISTEN_ADDRESS)
        self.ssl_cert = os.environ.get('SSL_CERT_NAME', Configuration.SSL_CERT)
        self.ssl_key_name = os.environ.get('SSL_KEY_NAME',
                                           Configuration.SSL_KEY)
        self.api_token = os.environ.get('API_TOKEN')

    @staticmethod
    def get_external_ip():
        return requests.get(IP_SERVICE_API_URL).text

    @staticmethod
    def create_config(ip_addr, port, listen_addr, ssl_cert, ssl_key,
                      api_token):
        config = {
            "bot": {"api_token": api_token},
            "server": {
                "host": ip_addr,
                "port": port,
                "listen": listen_addr,
                "ssl_cert": ssl_cert,
                "ssl_key": ssl_key
            }
        }
        with open('config.yml', 'w') as config_file:
            yaml.dump(config, config_file, default_flow_style=False)

    def get_parameters(self):
        return (self.ip_addr, self.port, self.listen, self.ssl_cert,
                self.ssl_key_name, self.api_token)

    @staticmethod
    def create_certs(cert_name, key_name, hostname, cert_days=1825):
        cmd = ['openssl', 'req', '-newkey', 'rsa:2048', '-sha256', '-nodes',
               '-keyout', '%s' % key_name, '-x509', '-days', '%s' % cert_days,
               '-out', '%s' % cert_name, '-subj',
               '/C=US/ST=New York/L=Brooklyn/O=NZT/CN=%s' % hostname]
        subprocess.run(cmd, check=True)


def main():
    config = Configuration()
    config.create_config(*config.get_parameters())
    config.create_certs(config.ssl_cert, config.ssl_key_name, config.ip_addr)

    subprocess.run(['python', 'bot.py'], check=True)

if __name__ == "__main__":
    main()
