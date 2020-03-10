import json


async def add(userid, response):
        with open("./db/daily_logs.json", "r") as db:
                data = json.load(db)
        with open("./db/daily_logs.json", "w") as db_2:
                data[response].append(str(userid))
                json.dump(data, db_2, indent=2)
                return

async def check(userid, response):
        with open("./db/daily_logs.json", "r") as db:
                data = json.load(db)
                for index in data[response]:
                        if str(index) == str(userid):
                                return(True)
        return(False)

async def clear():
        with open("./db/daily_logs.json", "w") as db_2:
                data = {
                        "413": [
                                ],
                        "offline": [
                                ],
                        "urltaken": [
                                ],
                        "idtaken": [
                                ],
                        "unablebump": [
                                ],
                        "invalid": [
                                ],
                        "noinvite": [
                                ],
                        "role": [
                                ]
                        }
                json.dump(data, db_2, indent=2)
                return
