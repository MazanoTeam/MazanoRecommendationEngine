from pymongo import MongoClient
from dotenv import load_dotenv


class LikesDB:
    def __init__(self, URI: str, db_name: str, collection_name: str):
        self.client = MongoClient(URI)
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]
        
    def get_user_likes(self, user_uuid: str, item_type: str):
        cursor = self.collection.find({
            "uuid": user_uuid
        })
        
        try:
            user = list(cursor)[0]
            return user['likes'][item_type]
        
        except (IndexError, KeyError):
            return None
        