from config import *
from models import *


class DbClient:
    "For Reading, Updating & Deleting Spreadsheet Content"

    def get_collection(self, name: str):
        "Returns The Collections Document (Query by - name)"
        res = database_client['raznesi_bot'][name]
        return res

    def get_user(self, user_id) -> User | None:
        "Fetch A Particular User"
        collection = self.get_collection('users')
        result = collection.find_one({"user_id": int(user_id)})
        return result

    def get_order(self, id):
        "Fetch A Particular Order"
        collection = self.get_collection('orders')
        # Retunrs only active orders
        result = collection.find_one({"buyer": id, "active": True})
        return result

    def get_order_by_msg_id(self, id):
        "Get order by a specific message ID"
        collection = self.get_collection('orders')
        # Retunrs only active orders
        result = collection.find_one({"msg_id": id})
        return result

    def create_update_user(self, user: User):
        "Create A New User"
        collection = self.get_collection("users")
        # Write To Collection
        result = collection.find_one({"user_id": user.user_id})  # Checker

        if result == None:
            res = collection.insert_one(user.__dict__)
        else:
            res = collection.update_one(
                {"user_id": user.user_id}, {"$set": user.__dict__})
        return res

    def create_update_order(self, order: Order):
        "Create Or Update Order"
        collection = self.get_collection("orders")
        # Write To Collection
        result = collection.find_one({"buyer": order.buyer})  # Checker

        if result == None:
            res = collection.insert_one(order.__dict__)
        else:
            res = collection.update_one(
                {"buyer": order.buyer}, {"$set": order.__dict__})
        return res

    def end_order(self, msg_id, status):
        "Close A Specific order"
        collection = self.get_collection('orders')
        # Retunrs only active orders
        result = collection.update_one(
            {"msg_id": msg_id}, {"$set": {"status": status}})
        return result


db_client = DbClient()
