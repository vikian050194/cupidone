from unittest import TestCase
from unittest.mock import call, patch
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
        expected_invocations = 7
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

    # TODO move to unit tests
    def test_complete_add(self, mock_print):
        complete = ["complete", "a"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("add")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_init(self, mock_print):
        complete = ["complete", "i"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("init")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_migration(self, mock_print):
        complete = ["complete", "m"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("migrate")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_migration_trello(self, mock_print):
        complete = ["complete", "migrate", "t"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("trello")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_migration_vanilla(self, mock_print):
        complete = ["complete", "migrate", "v"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("vanilla")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_build(self, mock_print):
        complete = ["complete", "b"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("build")
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_build_subcommands(self, mock_print):
        complete = ["complete", "build"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 2
        self.assertEqual(actual_invocations, expected_invocations)
        self.assertEqual(mock_print.call_args_list[0], call("todo"))
        self.assertEqual(mock_print.call_args_list[1], call("site"))
        mock_print.reset_mock()

    # TODO move to unit tests
    def test_complete_build_todo(self, mock_print):
        complete = ["complete", "build", "t"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("todo")
        mock_print.reset_mock()

            # TODO move to unit tests
    def test_complete_build_site(self, mock_print):
        complete = ["complete", "build", "s"]

        self.call(complete)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.assert_called_with("site")
        mock_print.reset_mock()

    def test_help(self, mock_print):
        help = ["help"]

        self.call(help)
        actual_invocations = len(mock_print.call_args_list)
        expected_invocations = 6
        self.assertEqual(actual_invocations, expected_invocations)
        mock_print.reset_mock()
