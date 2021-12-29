from pymongo import MongoClient
class DataBaseManager:
    def __init__(self, username: str = None, password: str = None):
        self.__client = MongoClient('localhost', username=username, password=password)
        self.__db = self.__client.conversationDB
        self.__collection = self.__db.conversations
    def read_all(self):
        return self.__collection.find().sort("timestamp")
    def write_in(self, message: str, client_token: str, timestamp: int):
        self.__insert = self.__collection.insert_one({"message": message, "client_token": client_token, "timestamp": timestamp})
        return self.__insert
    def delete_message(self, messageRecordId: str):
        # TODO
        pass