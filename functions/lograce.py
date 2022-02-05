import os
from classes.Race import Race

def lograce(race:Race) -> None:
    print ("Logged this Race!")
    print(race)
    return

def create_race_file(path: str) -> bool:
    if not isinstance(path, str):
        emessage = f"input path must be a str. Found type {type(path)}"
        raise Exception(emessage)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            emessage = f"Unable to create directory"

