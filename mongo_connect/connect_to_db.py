from pymongo import MongoClient

class LikesDB:
    def __init__(self, URI: str, db_name: str, collection_name: str):
        self.client = MongoClient(URI)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]
        
    def get_user_likes(self, user_uuid: str):
        cursor = self.collection.find({
            "user": user_uuid
        })
        print(cursor)
        
