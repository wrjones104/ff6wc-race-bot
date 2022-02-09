import functions.constants
import classes.Race
from functions.string_functions import parse_done_time
import datetime
import discord

class RaceRunner:
    """Contains information about a runner for a specific race"""

    def __init__(self) -> None:
        self._member = None
        self._race = None
        self._join_date = None
        self._start_date = None
        self._finish_date = None
        self._ready = False
        self._forfeit = False
        self._time_taken = None
        self._guild = None
        self._channel = None


    @property
    def member(self) -> discord.member.Member:
        """The discord Member"""
        return self._member

    @member.setter
    def member(self, input: discord.member.Member) -> None:
        """The discord Member"""
        if not isinstance(input, discord.member.Member):
            emessage = f"input must be a discord.member.Member. Found type {type(input)}"
            raise Exception(emessage)
        self._member = input

    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, input) -> None:
        if not isinstance(input, classes.Race.Race):
            emessage = f"input must be an FF6WC-raceroombot-Race. Found type {type(input)}"
            raise Exception(emessage)
        self._race = input

    @property
    def join_date(self) -> datetime.datetime:
        return self._join_date

    @join_date.setter
    def join_date(self, input:datetime.datetime) -> None:
        if not isinstance(input, datetime.datetime):
            emessage = f"input must be a datetime.datetime object. Found type {type(input)}"
            raise Exception(emessage)
        self._join_date = input

    @property
    def start_date(self) -> datetime.datetime:
        return self._start_date

    @start_date.setter
    def start_date(self, input:datetime.datetime) -> None:
        if not isinstance(input, datetime.datetime):
            emessage = f"input must be a datetime.datetime object. Found type {type(input)}"
            raise Exception(emessage)
        self._start_date = input

    @property
    def finish_date(self) -> datetime.datetime:
        return self._finish_date

    @finish_date.setter
    def finish_date(self, input:datetime.datetime) -> None:
        if not isinstance(input, datetime.datetime):
            emessage = f"input must be a datetime.datetime object. Found type {type(input)}"
            raise Exception(emessage)
        self._finish_date = input

    @property
    def ready(self) -> bool:
        return self._ready

    @ready.setter
    def ready(self, input:bool) -> None:
        if not isinstance(input, bool):
            emessage = f"input must be a bool. Found type {type(input)}"
            raise Exception(emessage)
        self._ready = input

    @property
    def forfeit(self) -> bool:
        return self._forfeit

    @forfeit.setter
    def forfeit(self, input:bool) -> None:
        if not isinstance(input, bool):
            emessage = f"input must be a bool. Found type {type(input)}"
            raise Exception(emessage)
        self._forfeit = input

    @property
    def time_taken(self) -> datetime.timedelta:
        if self._start_date is None:
            return None
        if self._forfeit:
            return None
        if self._finish_date is None:
            return None
        taken = self.finish_date - self.start_date
        self._time_taken = taken
        return self._time_taken

    @time_taken.setter
    def time_taken(self, input) -> None:
        emessage = f"time_taken is calculated from start_date and finish_date and cannot be set."
        raise Exception(emessage)

    @property
    def guild(self) -> discord.guild.Guild:
        return self._guild

    @guild.setter
    def guild(self, input:discord.guild.Guild) -> None:
        if not isinstance(input, discord.guild.Guild):
            emessage = f"input must be a discord.guild.Guild. Found type {type(input)}"
            raise Exception(emessage)
        self._guild = input

    @property
    def channel(self) -> discord.channel.TextChannel:
        return self._channel

    @channel.setter
    def channel(self, input:discord.channel.TextChannel):
        if not isinstance(input, discord.channel.TextChannel):
            emessage = f"input must be discord.channel.TextChannel. Found type {type(input)}"
            raise Exception(emessage)
        self._channel = input

    def __str__(self) -> str:
        output = ""
        output += f"Member:    {self.member}\n"
        output += f"Guild:     {self.guild}\n"
        output += f"Channel:   {self.channel}\n"
        output += f"Race:      {self.race.channel}\n"
        output += f"Join:      {self.join_date}\n"
        output += f"Start:     {self.start_date}\n"
        output += f"Finish:    {self.finish_date}\n"
        output += f"Ready:     {self.ready}\n"
        output += f"Forfeit?:  {self.forfeit}\n"
        output += f"TimeTaken: {self.time_taken}\n"
        output += "\n"
        return output

