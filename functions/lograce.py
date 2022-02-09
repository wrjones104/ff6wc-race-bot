import os
import shutil

#from tkinter import E
from classes.Race import Race
from functions.constants import TZ, RACE_PATH

def lograce(race:Race) -> None:
    output_file = create_race_file(RACE_PATH, race)
    print (f"Logged this race at {output_file}")
    print(race)
    print(race.results)
    return

def create_race_file(path: str, race:Race) -> str:
    if not isinstance(path, str):
        emessage = f"input path must be a str. Found type {type(path)}"
        raise Exception(emessage)

    if not isinstance(race, Race):
        emessage = f"input must be an FF6WC-raceroombot-Race. Found type {type(race)}"
        raise Exception(emessage)

    if not race.guild or not race.guild.id:
        emessage = f"Race does not have proper guild information.\n {race}\n"
        raise Exception(emessage)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            emessage = f"Unable to create directory {path}"
            raise Exception(emessage)

    if not path.endswith(os.sep):
        path += os.sep
    guild_path = path + str(race.guild.id)
    guild_path = os.path.abspath(guild_path)

    if not os.path.exists(guild_path):
        try:
            os.makedirs(guild_path)
        except Exception as e:
            emessage = f"Unable to create directory {guild_path}"
            raise Exception(emessage)

    filename = race.channel.name + "-" + race.opened_date.strftime("%Y-%m-%d") + ".json"
    filepath = guild_path + os.sep + filename
    if os.path.exists(filepath):
        counter = 0
        bkp_path = filepath + f".bkp_{str(counter).zfill(4)}"
        while os.path.exists(bkp_path):
            if counter > 9999:
                emessage = f"Tried to create 10,000 races with the same name and date in {guild_path}"
                raise Exception(emessage)
            counter += 1
            bkp_path = filepath + f".bkp_{str(counter).zfill(4)}"
        shutil.copyfile(filepath, bkp_path)

    # We should now have clean access to write to the output file
    with open(filepath, 'w') as f:
        js = race.toJSON()
        f.write(js)
    return filepath


