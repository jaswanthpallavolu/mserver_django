from firebase_admin import credentials, storage
import firebase_admin
import environ
from pathlib import Path

root = Path('.')
env = environ.Env()
environ.Env.read_env(root / '.env')

# path = root / 'serviceAccount.json'
config = {
    "type": "service_account",
    "project_id": env('PROJECT_ID'),
    "private_key_id": env("private_key_id"),
    "private_key": '-----BEGIN PRIVATE KEY-----\n' + env("private_key").replace('\\n', '\n') + '\n-----END PRIVATE KEY-----\n',
    "client_email": env("client_email"),
    "client_id": env("client_id"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": env("client_x509_cert_url")
}
cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred,
                              {"storageBucket": env('storageBucket'),
                               "databaseURL": env('databaseURL')})

bucket = firebase_admin.storage.bucket()
