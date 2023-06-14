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
    "<YOUR-SDK-HERE>"
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
