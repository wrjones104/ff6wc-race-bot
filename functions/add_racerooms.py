import discord
from discord.utils import get
import datetime
import random
import string

def add_racerooms(user, room_id, room_type, spoiler_room, ts):
    pass
    f = open("db/races.txt", "a")
    writemsg = str([user, room_id, room_type, spoiler_room, ts])+"\n"
    f.write(writemsg)
    f.close()