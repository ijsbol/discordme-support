import json

async def check(command):
        with open("./db/customcommands.json", "r") as command_db:
                new_data = json.load(command_db)
                if str(command) in str(new_data):
                      return(True)
                else:
                      return(False)

async def get_response(command):
        with open("./db/customcommands.json", "r") as command_db:
                new_data = json.load(command_db)
                for command_name in new_data:
                        if str(command_name) == str(command):
                                return(new_data[command_name])

async def change(command, new_response):
      with open("./db/customcommands.json", "r") as command_db:
            new_data = json.load(command_db)
      with open("./db/customcommands.json", "w") as command_db_2:
            new_data[str(command)] = str(new_response)
            json.dump(new_data, command_db_2, indent=2)
            return

async def create(command, response):
      with open("./db/customcommands.json", "r") as command_db:
            new_data = json.load(command_db)
      with open("./db/customcommands.json", "w") as command_db_2:
            new_data[str(command)] = str(response)
            json.dump(new_data, command_db_2, indent=2)
            return
