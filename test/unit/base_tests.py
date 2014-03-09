"""Test dateandtime's base functions."""


import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
    from StringIO import StringIO
else:
    import unittest
    from io import StringIO

from dateandtime.base import parse_args


class ArgumentParsingTests(unittest.TestCase):
    """Tests for cmd line argument parsing."""
    def setUp(self):
        """Reset default settings."""

        self.defaults = {
            "discordian": False,
            "eve_game": False,
            "eve_real": False,
            "help": False,
        }

    def tearDown(self):
        """Clean up any changes."""

        self.defaults = None

    def _test_parse(self, args=None):
        """Helper function."""

        return self.assertEqual(parse_args(args), self.defaults)

    def test_no_args(self):
        """Basic use case."""

        args = ["dateandtime"]
        self._test_parse(args)

    def test_literally_no_args(self):
        """This shouldn't be possible, but it shouldn't break anything."""

        self._test_parse()

    def test_one_arg(self):
        """Simple use case."""

        args = ["dateandtime", "-e"]
        self.defaults.update({"eve_game": True})
        self._test_parse(args)

    def test_two_args_the_same(self):
        """Shouldn't make a difference."""

        args = ["dateandtime", "-d", "--discordian"]
        self.defaults.update({"discordian": True})
        self._test_parse(args)

    def test_two_different_args_raise(self):
        """Should raise SystemExit."""

        args = ["dateandtime", "-r", "-e"]
        with self.assertRaises(SystemExit):
            parse_args(args)

    def test_three_raise_content(self):
        """Test the output of the sys exit being raised."""

        args = ["dateandtime", "-r", "-e", "-d"]
        with self.assertRaises(SystemExit) as error:
            parse_args(args)

        if sys.version_info < (3,):
            error_message = error.exception.message.strip()
        else:
            error_message = error.exception.code.strip()

        expected = (
            "Please limit yourself to a single calendar.\nI cannot display "
            "discordian, eve game and eve real at the same time :("
        )
        self.assertEqual(error_message, expected)

    def test_two_raise_content(self):
        """Test the content of the sys exit being raised."""

        args = ["dateandtime", "-r", "-d"]
        with self.assertRaises(SystemExit) as error:
            parse_args(args)

        if sys.version_info < (3,):
            error_message = error.exception.message.strip()
        else:
            error_message = error.exception.code.strip()

        expected = (
            "Please limit yourself to a single calendar.\nI cannot display "
            "discordian and eve real at the same time :/"
        )
        self.assertEqual(error_message, expected)

    def test_two_raise_content_two(self):
        """Test the ording of the sys exit being raised."""

        args = ["dateandtime", "-r", "-e"]
        with self.assertRaises(SystemExit) as error:
            parse_args(args)

        if sys.version_info < (3,):
            error_message = error.exception.message.strip()
        else:
            error_message = error.exception.code.strip()

        expected = (
            "Please limit yourself to a single calendar.\nI cannot display "
            "eve game and eve real at the same time :/"
        )
        self.assertEqual(error_message, expected)

    def test_help_message(self):
        """Ensure the test message looks correct."""

        args = ["dateandtime", "-h"]
        with self.assertRaises(SystemExit) as error:
            parse_args(args)

        if sys.version_info < (3,):
            error_message = error.exception.message.strip()
        else:
            error_message = error.exception.code.strip()

        expected = (
             "Dateandtime usage:\n  dateandtime [calendar] [-h/--help]\n"
            "Alternate calendars (usage flags):\n  Discordian: [-d, --discord,"
            " --discordian, --discordianism]\n  Eve (game): [-e, --eve, --eve-"
            "game]\n  Eve (real): [-r, --eve-real, --eve-is-real]"
        )
        self.assertEqual(error_message, expected)


if __name__ == "__main__":
    unittest.main()
