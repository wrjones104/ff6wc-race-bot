import os
import unittest
from functions.add_racerooms import *
from functions.string_functions import *

class TestFunctions(unittest.TestCase):
    """Test the functions in the functions directory"""
    def testRoomname(self):
        """Test for Roomname function"""
        name = "RoomName1"
        assert parse_roomname(name) == "roomname1"

        name = 'Z' * 29
        assert parse_roomname(name) == "zzzzzzzzzzzzzzzzzzzzzzzzzzzzz"

        roomname = parse_roomname()
        assert isinstance(roomname, str) and roomname.startswith('ff6wc-') and len(roomname) == 12 and roomname.lower() == roomname

        # ------------------
        # Failure assertions - These things should raise exceptions
        # ------------------
        name = 37
        with self.assertRaises(Exception):
            assert parse_roomname(name)

        name = ''
        with self.assertRaises(Exception):
            assert parse_roomname(name)

        name = 'Z' * 30
        with self.assertRaises(Exception):
            assert parse_roomname(name)

        name = 'Z' * 7377
        with self.assertRaises(Exception):
            assert parse_roomname(name)

    def testParseCommand(self):
        """
        Test the command parser. This doesn't test to make sure the command exists or is correct, but tests
            that the format is correct
        """
        input = "!join myrace-sync"
        assert parse_command(input) == {'join': {'room': ('myrace-sync',)}}

        input = "!openrace -name TestRoom1 -s 7"
        assert parse_command(input) == {'openrace': {'name': ('TestRoom1',), 's': ('7',)}}

        input = "!done 1:23:04"
        assert parse_command(input) == {'done': {'time': ('1:23:04',)}}

        # This is a mess of a command, but its syntax is valid
        input = "!openrace -name TestRoom1 -s 7 done 3:18:09"
        assert parse_command(input) == {'openrace': {'name': ('TestRoom1',), 's': ('7', 'done', '3:18:09')}}

        # Check for multiple spaces
        input = "!openrace -name TestRoom1 -s       7"
        assert parse_command(input) == {'openrace': {'name': ('TestRoom1',), 's': ('7',)}}

        # Check for trailing spaces
        input = "!openrace -name TestRoom1 -s 7        "
        assert parse_command(input) == {'openrace': {'name': ('TestRoom1',), 's': ('7',)}}

        # Check for leading spaces
        input = "   !openrace -name TestRoom1 -s 7        "
        assert parse_command(input) == {'openrace': {'name': ('TestRoom1',), 's': ('7',)}}

        # Test crazy alternate dashes - https://www.compart.com/en/unicode/category/Pd
        for dash in dashes:
            input = f"!openrace {dash}name TestRoom1 -s 7"
            assert parse_command(input) == {'openrace': {'name': ('TestRoom1',), 's': ('7',)}}

        # ------------------
        # Failure assertions - These things should raise exceptions
        # ------------------

        # Make sure input is a string
        input = 37
        with self.assertRaises(Exception):
            parse_command(input)

        # Test not starting with !
        input = "openrace -name TestRoom1 -argument2 Something"
        with self.assertRaises(Exception):
            parse_command(input)

        # Check for empty command
        input = "! openrace -name TestRoom1 -s 7        "
        with self.assertRaises(Exception):
            parse_command(input)

        # Test having multiple commands
        input = "!openrace -name TestRoom1 -argument2 Something !OtherCommand"
        with self.assertRaises(Exception):
            parse_command(input)

        input = "!openrace -name TestRoom1 -argument2 Something !OtherCommand !!!!!!!! !! !"
        with self.assertRaises(Exception):
            parse_command(input)


