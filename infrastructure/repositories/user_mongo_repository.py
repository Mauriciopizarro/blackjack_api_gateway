from pymongo import MongoClient
from bson.objectid import ObjectId
from domain.exceptions import UserExistent, NotExistentUser
from domain.interfaces.user_repository import UserRepository
from domain.user import UserInDB, UserPlainPassword


class UserMongoRepository(UserRepository):

    instance = None

    def __init__(self):
        self.db = self.get_database()

    # Patron singleton
    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    @staticmethod
    def get_database():
        client = MongoClient("mongodb://mongo:27017/blackjack")
        return client['api_gateway']["users"]

    def get_by_username(self, username):
        user_dict = self.db.find_one({"username": username})
        if user_dict is None:
            raise NotExistentUser()
        user_dict.update({'_id': str(user_dict.get('_id'))})
        user_dict["id"] = user_dict.pop('_id')
        return UserInDB(**user_dict)

    def save_user(self, user: UserPlainPassword):
        user_dict = self.db.find_one({"username": user.username})
        if user_dict:
            raise UserExistent()
        hashed_password = user.get_hashed_password()
        user_id = self.db.insert_one({"username": user.username, "email": user.email, "hashed_password": hashed_password})
        return UserInDB(hashed_password=hashed_password, id=str(user_id.inserted_id), username=user.username, email=user.email)

    def update_password(self, user: UserInDB):
        user_dict = user.dict()
        user_dict.pop("id")
        self.db.find_one_and_update({"_id": ObjectId(user.id)}, {"$set": user_dict})
