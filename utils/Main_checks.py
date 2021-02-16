"""
If account doesn't exists,
Then, make a new one,
Else, don't do antthing
"""

import json

DB_PATH = "Json\db.json"


class MainChecks():
    def __init__(self, *_):
        print("Inside __init__")
        self._ = _

    def load_data(self) -> dict:
        """Loads data"""
        print("Inside load_data")
        with open(DB_PATH, "r") as file:
            return json.load(file)

    def account_exist(self, user_id: str):
        """Checks whether the account exist"""
        data = self.load_data()
        if str(user_id) not in data:
            print("created new account")
            return self.open_account(str(user_id))

    def open_account(self, user_id: str) -> None:
        """A new account is being made"""
        print("Inside open_account")
        data = self.load_data()

        data[user_id] = {}
        data[user_id]["bank"] = 100.00
        data[user_id]["wallet"] = 100.00

        return self.save_data(data)

    def save_data(self, data) -> None:
        """Saving the current state of the account"""
        print("Inside save_data")
        with open(DB_PATH, "w") as file:
            json.dump(data, file, indent=4)
