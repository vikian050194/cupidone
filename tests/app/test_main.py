from unittest import TestCase, skip
from unittest.mock import patch, call
from tempfile import TemporaryDirectory

from cupidone.main import main
from cupidone.configuration import make_config, OutputFlagValues


@patch("builtins.print")
class TestMain(TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        directory=self.temp_dir.name
        output=OutputFlagValues.HUMAN
        configuration = make_config(directory=directory, output=output)
        self.call = lambda options: main(options=options, configuration=configuration)

    def tearDown(self):
        self.temp_dir.cleanup()

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_command_is_missed(self, mock_print):
        empty = []

        self.call(empty)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("ERROR: command is missed, please try \"help\"")
        mock_print.reset_mock()

    def test_unknown_command(self, mock_print):
        invalid = ["not_a_valid_option"]

        self.call(invalid)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with('ERROR: command "not_a_valid_option" is not found, please try "help"')
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_all(self, mock_print):
        complete = ["complete"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 2
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("help")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_version(self, mock_print):
        complete = ["complete", "v"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("version")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_help(self, mock_print):
        complete = ["complete", "h"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("help")
        mock_print.reset_mock()

    def test_help(self, mock_print):
        help = ["help"]

        self.call(help)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 4
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.reset_mock()
