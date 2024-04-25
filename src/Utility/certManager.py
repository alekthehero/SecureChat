from OpenSSL import crypto
import os

def CreateSelfSignedCert(certDir):
    if not os.path.exists(certDir):
        os.makedirs(certDir)

    certFile = os.path.join(certDir, 'cert.pem')
    keyFile = os.path.join(certDir, 'key.pem')

    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    #Generate the cert
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "Florida"
    cert.get_subject().L = "Miami"
    cert.get_subject().O = "University of Miami"
    cert.get_subject().OU = "ECE Department"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    open(certFile, "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8'))
    open(keyFile, "wt").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode('utf-8'))

    print('Created self signed certificate')

CreateSelfSignedCert('certs')

