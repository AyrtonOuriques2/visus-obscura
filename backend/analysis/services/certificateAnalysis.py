import ssl
import socket
from datetime import datetime


async def certificateCheck(url: str):
    obj = ssl.create_default_context()
    try:
        with socket.create_connection((url, 443), timeout=5) as sock:
            with obj.wrap_socket(sock, server_hostname=url) as wpsock:
                cert = wpsock.getpeercert()
                
                if cert:
                    subject = dict(x[0] for x in cert['subject'])
                    issued_to = subject.get('commonName', '')
                    issuer = dict(x[0] for x in cert['issuer'])
                    issued_by = issuer.get('commonName', '')

                    not_before = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
                    not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                    now = datetime.now()
                    return {
                        "hostname" : url,
                        "https_supported": True,
                        "cert_present": True,
                        "valid_now": not_before <= now <= not_after,
                        "expires_on": not_after,
                        "expires_in_days": (not_after - now).days,
                        "issued_to": issued_to,
                        "issued_by": issued_by,
                        "subject": subject,
                        "issuer": issuer,
                    }

    except Exception as e:
        return {
            "hostname": url,
            "https_supported": False,
            "cert_present": False,
            "error": str(e)
        }