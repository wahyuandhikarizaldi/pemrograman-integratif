import grpc
from concurrent import futures
import rpc_pb2
import rpc_pb2_grpc
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time


class FirestoreServicer(rpc_pb2_grpc.FirestoreServicer):
    def __init__(self):
        self.db = firestore.client()
        
    def AddDocument(self, request, context):
        doc_ref = self.db.collection(u'names').document(request.code)
        doc_ref.set({"name": request.name})
        return rpc_pb2.DocumentResponse(name=request.name)
        
    def GetDocument(self, request, context):
        doc_ref = self.db.collection(u'names').document(request.code)
        doc_data = doc_ref.get().to_dict()
        return rpc_pb2.DocumentResponse(name=doc_data['name'])
    
    def UpdateDocument(self, request, context):
        doc_ref = self.db.collection(u'names').document(request.code)
        doc_ref.set({"name": request.name}, merge=True)
        return rpc_pb2.Empty()

    def DeleteDocument(self, request, context):
        doc_ref = self.db.collection(u'names').document(request.code)
        doc_ref.delete()
        return rpc_pb2.Empty()

def serve():
    
    # Firebase Admin SDK here
    key = {
    "type": "service_account",
    "project_id": "grpc-ada9b",
    "private_key_id": "86f38cdb21f811c0a23b5d1e8603bd9f6fce538d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDWB5CI+5/TXQtB\nLgdCVLWZgo/Xq4WWaRNG0eDa7gDy9JX3tSgRDSb8cmENeCDDC8FbnQ1427urXKJI\nY/TCMDFLN2CgH8b74vHzisvN+j2sTlK9MFoXKa+u3EwnaKiAoEiUd+3fIUXHgFhK\n11xtlKc4bG7+G51wPbhRjvyFuIwVGr2R0HI6AloRMScB++tyfL7uHfEPlx8lwZFV\n7XvdFEKkaoylKAliQdjzCMMpq6JFUKReoHztUkwYfLmggdb9UWe4ZlbCB41wJetn\nj6uuLOu9Cm6VLvYsLBBLGNflM9qVrBxFbzS+TaSWguMjPMcCM5TfiBLK9rz6w8R7\ne73vhptnAgMBAAECggEAaEbDOpotolMAur7sNnsDB0m/PzqIGWIUTDrRLJksyTI1\nJrySSsx3pCMt+dv/Skgd6r6345xa8QBu6Ioao8nLGnRelWUmE27cpuWGqlIzXhHC\n6f32xrY+rBkU2VZ6UkDFW+Caek3Bq5NycPRASftVBX5/DTrzF85aURIzIgtp5JWA\ng9ernu/Ljw1aNKLJDeAiiDzyVG3cxcyHtvkj6Z4VB8wzlEHqFbTZMtuD1f02tzhF\nL+4U71gpwG/Cy90OlfiNfIA/waD/vJobuwjl+GmNvVQ2oVUEnv2ArehzKpLBpTOs\nVMrgqhEZ6b71XtDoxMnXeI5jLfClFuSdar5wRNOnAQKBgQDvoElr5nRRGaWk3Vea\nmhiwweGUkyr/8dqBf5jaoyiMeHAFSnunc+ybOlC/iygyAKqj0BAjFPN7lul3T0lo\nC3BDvJfili6x5w6V/dWbV+TFluv+bG3zD0YvQkCX/USY+QttV+DizMip0lmIirSh\ntOr348LQlS56E0yLF1TDj6aAQQKBgQDkp4YpwlBT/QFvr9WcMFVtmDRCTkWYkzBI\nLCS51YJXBUavLoA0AnMTOyBZTG//lhEQq6hIzfRt0ky6FhWRy/7XhRnVJwO1V9lC\nWqoycv0KHM2Knuc5YCHOBYxpQJO+C1r3b1Fwc1t7Hsjo9QD9R9/7dX5zKZzxPcC5\n+0zQDDyxpwKBgGlTJLJ+mwXCpiIvAAB+VvfqYEKz5SSWo5pkAUWojXwgu+w3bt6N\nf6RDH5bxjXtc+6QBIfapkNPz4y6D9Rn8XR4I2SHJLUEY9DpNVgRvv6hxy80Kz9EU\nF59SGZ40vmAWp0UqaTiHFnQ+dwgjH34sTVMkE08nI0SZEv3YBXPnwiGBAoGAJhz2\ndAd7tEQ79Q3uITa9RqNUMqkxWJlQNveEt6UrMK4kdhbeL80ouU/luHzRPl0ZQxoZ\n1ujdkWC4gVwlBERomiwJfkoeiB+4iyLps7cPDpx2dmC+UgYAHIM4QGMPPWJPK2dW\nv9O6r+8Vth8ApzdP0m5nQXLyQhP1CAsnZpZjl4kCgYEA6P556hUIeL8W33GYFFqb\nelWEz9tF7w97ySTJCY1B3VXukAyd9kc/LaG/tHLJqe9o7nfsmYZl6OF9fkE/IIgm\nr+AeEFCLiFNbq5+mVR6+/zKvKT0cW/RgaPaIWj7GTzl8Z+Veajk8Ctz7HVbmHKRi\nGIXRN2h1ahANmX8ZIhkXCLE=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-73d11@grpc-ada9b.iam.gserviceaccount.com",
    "client_id": "118417854839209851509",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-73d11%40grpc-ada9b.iam.gserviceaccount.com"
    }
    # Initialize Firebase SDK
    cred = credentials.Certificate(key)
    firebase_admin.initialize_app(cred)
    
    # Create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer to server
    rpc_pb2_grpc.add_FirestoreServicer_to_server(FirestoreServicer(), server)
    
    # Start the server
    server.add_insecure_port('[::]:50051')
    server.start()
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()