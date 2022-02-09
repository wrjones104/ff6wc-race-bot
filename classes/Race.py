
import discord
import datetime
import time

from functions.constants import TZ
from functions.generate_z_score import generate_z_score
import functions.constants

class Race:
    """An object to store races"""
    from classes import RaceRunner
    def __init__(self, in_message, in_channel)->None:
        self._channel = None
        self._guild = None
        self._creator = None
        self._url = None
        self._admins = set(functions.constants.ADMINS)
        self._type = None
        self._members = {}
        self._opened_date = None
        self._closed_date = None
        self._race_start_date = None
        self._isHiddenSeed = False
        self._comments = ""
        self._results = ""
        self._closed = False

        if not isinstance(in_message, discord.message.Message):
            emessage = f"message must be a discord.message.Message. Found type {type(input)}"
            raise Exception(emessage)
        if not isinstance(in_channel, discord.channel.TextChannel):
            emessage = f"channel must be a discord.channel.TextChannel. Found type {type(input)}"
            raise Exception(emessage)

        self.creator = in_message.author
        self.admins.add(self.creator.id)
        self.guild = in_message.guild
        self.channel = in_channel
        self.opened_date = datetime.datetime.now(TZ)



    @property
    def channel(self) -> discord.channel.TextChannel:
        return self._channel

    @channel.setter
    def channel(self, input:discord.channel.TextChannel) -> None:
        if not isinstance(input, discord.channel.TextChannel):
            emessage = f"input should be a discord.channel.TextChannel. Found type {type(input)}"
            raise Exception(emessage)
        self._channel = input

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
    def creator(self) -> discord.member.Member:
        return self._creator

    @creator.setter
    def creator(self, input:discord.member.Member) -> None:
        if not isinstance(input, discord.member.Member):
            emessage = f"input should be a discord.member.Member. Found type {type(input)}"
            raise Exception(emessage)
        self._creator = input

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, input:str) -> None:
        if not isinstance(input, str):
            emessage = f"input should be a str. Found type {type(input)}"
            raise Exception(emessage)
        if not input.upper().startswith("HTTP") or "/seed/" not in input:
            emessage = f"input doesn't appear to be a valid seed link. Found {input}"
            raise Exception(emessage)
        self._url = input


    @property
    def admins(self) -> set:
        return self._admins

    @admins.setter
    def admins(self, input) -> None:
        #TODO - Check against channel admins - WD42 2022-01-31
        pass

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, input:str) -> None:
        if not isinstance(input, str):
            emessage = f"input should be type str. Found type {type(input)}"
            raise Exception(emessage)
        if not input.strip().lower() in functions.constants.RACETYPES:
            emessage = f"input must be one of: {functions.constants.RACETYPES}"
            raise Exception(emessage)
        self._type = input
        if self.type == functions.constants.RACETYPE_HIDDENSEED:
            self._isHiddenSeed = True
        else:
            self._isHiddenSeed = False

    @property
    def members(self) -> dict:
        return self._members

    @members.setter
    def members(self, input) -> None:
        emessage = "Race.members cannot be set directly. Use the addRacer and removeRacer methods."
        raise Exception(emessage)

    @property
    def opened_date(self) -> datetime.datetime:
        return self._opened_date

    @opened_date.setter
    def opened_date(self, input: datetime.datetime) -> None:
        if not isinstance(input, datetime.datetime):
            emessage = f"input should be datetime.datetime. Found type {type(input)}"
            raise Exception(emessage)
        self._opened_date = input

    @property
    def closed_date(self) -> datetime.datetime:
        return self._closed_date

    @closed_date.setter
    def closed_date(self, input) -> None:
            emessage = f"closed_date is set automatically when the race is closed"
            raise Exception(emessage)

    @property
    def race_start_date(self) -> datetime.datetime:
        return self._race_start_date

    @race_start_date.setter
    def race_start_date(self, input:datetime.datetime) -> None:
        if not isinstance(input, datetime.datetime):
            emessage = f"input should be datetime.datetime. Found type {type(input)}"
            raise Exception(emessage)
        self._race_start_date = input

    @property
    def isHiddenSeed(self) -> bool:
        return self._isHiddenSeed

    @isHiddenSeed.setter
    def isHiddenSeed(self, input:bool) -> None:
        emessage = "isHiddenSeed is automatically set by Race.type()"
        raise Exception(emessage)

    @property
    def comments(self) -> str:
        return self._comments

    @comments.setter
    def comments(self, input:str) -> None:
        if not isinstance(input, str):
            emessage = f"input should be str. Found type {type(input)}"
            raise Exception(emessage)
        self._comments = input

    @property
    def results(self) -> str:
        return self._results

    @results.setter
    def results(self, input:bool) -> None:
        emessage = "results is automatically set when the race is closed"
        raise Exception(emessage)


    def close(self) -> None:
        """Closes the race"""
        self._closed_date = datetime.datetime.now(TZ)

        times = {}
        results = []
        for member in self.members.keys():
            times[self.members[member].time_taken] = member
        counter = 1
        for time in sorted(times.keys()):
            runner = times[time]
            results.append((counter,runner,time))
        self._results = results

    def addRacer(self, input:RaceRunner) -> None:
        """Adds a RaceRunner to this Race.

        """
        from classes import RaceRunner
        if not isinstance(input, RaceRunner.RaceRunner):
            emessage = f"input should be an FF6WC-raceroombot-RaceRunner. Found type {type(input)}"
            raise Exception(emessage)
        self._members[input.member.name] = input

    def removeRacer(self, input:RaceRunner) -> None:
        """Removes a RaceRunner from this Race.

        """
        from classes import RaceRunner
        if not isinstance(input, RaceRunner.RaceRunner):
            emessage = f"input should be an FF6WC-raceroombot-RaceRunner. Found type {type(input)}"
            raise Exception(emessage)
        if input in self._members:
            del self._members[input.member.name]

    def toJSON(self) -> str:
        output = ''
        output += f'"guild":{self.guild.name},'
        output += f'"channel":{self.channel.name},'
        output += f'"creator":{self.creator.name},'
        output += f'"url":{self.url},'
        output += f'"type":{self.type},'
        output += f'"admins":[' + (',').join([str(admin) for admin in self.admins]) + '],'
        output += f'"members":[' + (',').join([self.members[member].member.name for member in self.members.keys()]) + '],'
        output += f'"date_opened":{self.opened_date},'
        output += f'"date_started":{self.race_start_date},'
        output += f'"date_closed":{self.closed_date},'
        output += f'"comments":"' + self.comments.replace("\"", "\'") + '"'
        output += f'"results:["'
        result_txt = []
        for result in self.results:
            result_txt.append(f"({result[0], result[1], result[2]})")
        output += (",").join(result_txt) + "]"
        output += "}"
        return output

    def getResults(self) -> str:
        output = "`"
        times = {}
        for member in self.members.keys():
            times[self.members[member].time_taken] = member
        counter = 1
        for time in sorted(times.keys()):
            output += f"{counter} - {times[time]} -- {time}\n"
        output += "`\n"
        return output


    def __str__(self) -> str:
        output = ""
        output += f"Guild:        {self.guild}\n"
        output += f"Channel:      {self.channel.name}\n"
        output += f"Creator:      {self.creator}\n"
        if not self.isHiddenSeed:
            output += f"Seed URL:     {self.url}\n"
        else:
            output += f"Seed URL:     Hidden\n"
        output += f"Admins:     \n"
        for admin in self.admins:
            output += f"    {str(admin)} ... {str(self.guild.get_member(admin))}\n"
        output += f"Type:         {self.type}\n"
        output += f"Members:     \n"
        if not self.members or len(self.members) == 0:
            output += "    No one has joined this race\n"
        else:
            for member in self.members.keys():
                output += f"    {self.members[member].member.name}\n"
        output += f"Date Opened:  {self.opened_date} ET\n"
        output += f"Date Started: "
        if self.race_start_date:
            output += f"{self.race_start_date} ET\n"
        else:
            output += "Not yet started\n"

        output += f"Date Closed:  "
        if self.closed_date:
            output += f"{self.closed_date} ET\n"
        else:
            output += "Not yet closed\n"

        output += f"Comments:     {self.comments}\n"
        output += "\n"
        return output

