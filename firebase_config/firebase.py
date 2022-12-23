from firebase_admin import credentials, storage
import firebase_admin


# path = root / 'serviceAccount.json'
config = {
    "type": "service_account",
    "project_id": "mrsystem-17d1b",
    "private_key_id": "4fde82d37cfb655732e62791269c335a4d9789cb",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC2mURE/s3gkpPk\ns5txn21d0WxflN9brOn6y/iLd9epZ15t8OP6kGLkM/pCsq3LVUz4DcH0QMLqMZ1W\nzgKuvSZ719tsVkr4gnzJhx9JIMj8srg9lMTAr1uaibWRWgPvAOiZjNr8n1f6ECnt\n1apyykri+5KmWiZ4IjhouLt2ykvihGgTBWzW7WLocwfjEPRigdTdaKIrDRsWODl3\nB8oF8i9y13+VYGcsqr4W5zKuCEV9TSpW+y3e+poUwEugEtzaTLg1WSLx+u0dzDRQ\nqKvKrGk5LlEIYvJGmX25uZ//Y3grHP6tuVEHi8t/ziuKtpM4/ik4f0mWiQDl43jr\nQ1E1evSvAgMBAAECggEAJWXNoC3pn5GVvbT1ZLeI0Dq4rfjRKDcJcua8oF/qqRT1\nN6IrJyHURzXID0oGI0t0qKc0rqBm600/Esy9quktjRbAJ3ejAjPDeAj3JOSUlYDL\nED28cFRZ+BQ1PjBH9vbiLLS3Ex9Vhu8xjzcAImOBI+zvc6eqEle74uLW7jTvhtRL\nScjxaGQ4b0PX3GI0mDTcckNBisY3YlxxD7j3Lci85MO7GpeFLpu6RtBiS1Z2DfeR\n/f7NIZM0p5WhPp0awZ9i+DEYA+ovdBPibOqqQocydcCK4o7eaHgLOP+fhGX+cdaD\nGr2N8xEl8YFRkwJyBhUdhSmTtfWjndiQNy7duOhvwQKBgQDzJ1ZqAQFYMAhgTFM7\n/3Mvd30AyIdjLdzlQ5BGP9AP9kYlfsVaAOUvfagPjchdXoK07JmgZK+Khe6EUMrw\nVDwLhNUY59Bf/pd8F+mN5jSwzEM42x451Zgo4eFh+RDFhIIKz/fz8dcKZLUwEgY0\no4YeDbYwuUgccdXorLq2TFiTQQKBgQDAPuvDQFC1qFLeb9dwnASXjJYCI4pIgQQX\nzhPCFqPDvQ8UfJzA0k33JLreIIzHwXUZxWr2ZcseTg2yqyzG2eyKQLFZ9nEEVrqb\nsWz/OGMkNuLS7D7gGw5dIRrcsCJozjNVQ7HOcIlpdwp3dvjYGnyyAfWHYP/TRPM7\nliQwwfm77wKBgQCDtwJzh7nfuJ1A9Pd9n8IYq2R2gSn9ysFHHBNSSoz9qI2VEBf9\nylBcKnhYfJhWI7UwJp6NqR0CL8zlthJIn4irQLhitmhFJ9eNbDKjIFnYj722VdQI\nxjCXrMx3UwEHzeDX1JJffdjcE3Om54yfBRnIu+q+eA+dAPk8Ah1eVPsCQQKBgCid\nooXP0r1uYIOqMWQTMk0qYI73H0IOL+UvnrEEw3iZOtRjN2Lti5dJZUmEqvmQ/8KA\nGQcRnoY6i15SF9WzOOxEmrOdA2edQzOdmp+ZNCj0h5t0WhxS2wgF9HznoX1vAx1i\nffBVilKD2ew/cHeHsQySqWL+tU3XZWQTZnX+pVp1AoGBAIf/JBDuJBBf+1hWNzfn\nE/GjzqMmSVsAtjknFzx+ocAPRDJX9ap+3FnW3PtFKp32kGD74lN2v0zFIJ9Is169\nB9/jCrCrxYp4t5LTM+dUShI67jXwdZ6dMfUpI5WEkLKOwpq30w26H8UMVLol6hT6\nyDI+gAOijFeHZ1iZ1H2dTn5Y\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-vh80f@mrsystem-17d1b.iam.gserviceaccount.com",
    "client_id": "106763338259546029023",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vh80f%40mrsystem-17d1b.iam.gserviceaccount.com"
}
cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred,
                              {"storageBucket": "mrsystem-17d1b.appspot.com",
                               "databaseURL": "https://mrsystem-17d1b-default-rtdb.firebaseio.com/"})

bucket = firebase_admin.storage.bucket()


# config = {
#     "apiKey": "AIzaSyA0EqLjFmzulGl0hwXyi6M2Yp0OoZIf_Xw",
#     "authDomain": "mrsystem-17d1b.firebaseapp.com",
#     "projectId": "mrsystem-17d1b",
#     "storageBucket": "mrsystem-17d1b.appspot.com",
#     "messagingSenderId": "549133703456",
#     "appId": "1:549133703456:web:2579d8beec9ce5ec999f45",
#     "serviceAccount": path,
#     "databaseURL": "https://mrsystem-17d1b-default-rtdb.firebaseio.com/"
# }

# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()

# print(storage.child('awardTags_11.06.pkl'))
# print(storage.list_files())
