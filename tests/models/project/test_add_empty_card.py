from unittest.mock import call
from cupidone.models import ProjectModel
from cupidone.views.message import InfoView

from ..model_test_case import ModelTestCase


class TestProjectModelAddEmptyCardMethod(ModelTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def model_class(self):
        return ProjectModel

    def test_no_cards(self):
        files = dict()
        self.files_to_return(files)
        self.now_to_return()

        view: InfoView = self.model.add_empty_card()

        self.assertEqual(view.value, "0001.md was added")
        # self.fm.write_card
        # self.assertEqual()
        actual_invocations = len(self.fm.write_card.call_args_list)
        expected_invocations = 1
        self.assertEqual(actual_invocations, expected_invocations)
        # self.fm.write_card.assert_called_with("help")
        lines = self.fm.write_card.call_args_list[0][0][1]
        for line in lines:
            if line.startswith("# "):
                self.assertEqual(line, "# New card title\n")
            if line.startswith("Created at"):
                self.assertEqual(line, "Created at: `2026-01-01T00:00:00`\n")
            if line.startswith("Type"):
                self.assertEqual(line, "Type: `bug`, `tech`, `business`, `marketing`\n")
            if line.startswith("State"):
                self.assertEqual(line, "State: `backlog`\n")

    def test_one_card(self):
        files = {
            "0001.md": "dummy test content"
        }
        self.files_to_return(files)

        view: InfoView = self.model.add_empty_card()

        self.assertEqual(view.value, "0002.md was added")
