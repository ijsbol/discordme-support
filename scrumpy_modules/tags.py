import json

async def get_info(tagname):
        with open("./db/tags.json", "r") as user_db_file:
                new_data = json.load(user_db_file)
                for userid_db in new_data:
                        if str(userid_db) == str(tagname):
                                return(new_data[tagname])
        return("None")

async def create(tagname, info):
      with open("./db/tags.json", "r") as user_db_file:
            new_data = json.load(user_db_file)
      with open("./db/tags.json", "w") as user_db_file_2:
            new_data[str(tagname)] = info
            json.dump(new_data, user_db_file_2, indent=2)
async def delete(tagname):
      with open("./db/tags.json", "r") as user_db_file:
            new_data = json.load(user_db_file)
      with open("./db/tags.json", "w") as user_db_file_2:
            new_data[str(tagname)] = "None"
            json.dump(new_data, user_db_file_2, indent=2)
