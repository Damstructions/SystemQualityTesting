"""Allow an otherwise valid TLS certificate whose only fault is the date.

Chrome's ERR_CERT_DATE_INVALID is a date check. The suite still requires the
default trust store to accept the chain and the leaf name to match the host.
Only that leaf key is then exempted, through Chrome's SPKI allow-list.
"""

import base64
import hashlib
import socket
import ssl
from urllib.parse import urlsplit

# OpenSSL: X509_V_ERR_CERT_NOT_YET_VALID, X509_V_ERR_CERT_HAS_EXPIRED.
_DATE_ERRORS = {9, 10}


def chrome_args_for_date_only(base_url):
    """Return Chrome launch args that ignore a date error on a good certificate.

    An empty list means the certificate needs no date exception, or it failed
    a check other than the date and must stay rejected.
    """
    host = urlsplit(base_url).hostname
    if not host or not _date_is_only_trust_error(host):
        return []
    der = _leaf_der(host)
    if not _name_matches(der, host):
        return []
    spki = base64.b64encode(hashlib.sha256(_spki_der(der)).digest()).decode("ascii")
    return [f"--ignore-certificate-errors-spki-list={spki}"]


def _date_is_only_trust_error(host):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, 443), timeout=20) as sock:
            with context.wrap_socket(sock, server_hostname=host):
                return False
    except ssl.SSLCertVerificationError as exc:
        return exc.verify_code in _DATE_ERRORS
    except OSError:
        return False


def _leaf_der(host):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((host, 443), timeout=20) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls:
            return tls.getpeercert(binary_form=True)


def _name_matches(der, host):
    names = _dns_names(der)
    if names:
        return any(_dns_matches(name, host) for name in names)
    return any(_dns_matches(name, host) for name in _common_names(der))


def _dns_matches(pattern, host):
    pattern = pattern.lower().rstrip(".")
    host = host.lower().rstrip(".")
    if pattern == host:
        return True
    if pattern.startswith("*."):
        suffix = pattern[1:]
        return host.endswith(suffix) and "." not in host[: -len(suffix)]
    return False


def _spki_der(der):
    fields = _tbs_fields(der)
    # v3 certificates carry an explicit version tag before the serial number.
    index = 6 if fields[0][0] == 0xA0 else 5
    return fields[index][1]


def _dns_names(der):
    fields = _tbs_fields(der)
    wrapped = next((value for tag, _raw, value in fields if tag == 0xA3), b"")
    if not wrapped:
        return []
    names = []
    for _tag, _raw, extension in _items(_sequence_body(wrapped)):
        parts = _items(extension)
        oid = next(value for tag, _raw, value in parts if tag == 0x06)
        if oid != bytes((0x55, 0x1D, 0x11)):
            continue
        payload = next(value for tag, _raw, value in parts if tag == 0x04)
        for tag, _raw, value in _items(_sequence_body(payload)):
            if tag == 0x82:
                names.append(value.decode("ascii"))
    return names


def _common_names(der):
    fields = _tbs_fields(der)
    subject = fields[5][2] if fields[0][0] == 0xA0 else fields[4][2]
    names = []
    for _tag, _raw, rdn in _items(subject):
        for _tag, _raw, pair in _items(rdn):
            parts = _items(pair)
            oid = next(value for tag, _raw, value in parts if tag == 0x06)
            # 2.5.4.3 commonName
            if oid == bytes((0x55, 0x04, 0x03)):
                text = next(value for tag, _raw, value in parts if tag != 0x06)
                names.append(text.decode("utf-8", "replace"))
    return names


def _tbs_fields(der):
    certificate = _sequence_body(der)
    tbs = _items(certificate)[0][2]
    return _items(tbs)


def _sequence_body(tlv):
    _tag, value, _raw = _read(tlv, 0)
    return value


def _items(data):
    items = []
    index = 0
    while index < len(data):
        tag, value, raw = _read(data, index)
        items.append((tag, raw, value))
        index += len(raw)
    return items


def _read(data, index):
    start = index
    tag = data[index]
    index += 1
    length = data[index]
    index += 1
    if length & 0x80:
        count = length & 0x7F
        length = int.from_bytes(data[index:index + count], "big")
        index += count
    end = index + length
    return tag, data[index:end], data[start:end]
