from unittest import TestCase
from unittest.mock import create_autospec, Mock

from datetime import datetime, date

from cupidone.managers.file_manager import AbstractFileManager, FileManager
from cupidone.managers.time_manager import AbstractTimeManager, TimeManager
from cupidone.models.base import AbstractModel


def get_file_manager_spec():
    fm: AbstractFileManager = create_autospec(spec=FileManager, spec_set=True, instance=True)
    return fm


class ModelTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fm: AbstractFileManager = get_file_manager_spec()
        self.tm: AbstractTimeManager = TimeManager()

        self.model = self.model_class(fm=self.fm, tm=self.tm)

    def setUp(self):
        self.fm.reset_mock()
        # self.fm.load_project = Mock(return_value="test_project")
        # self.fm.load_actions = Mock(return_value=[])
        # config = Config(day_limit=8, total_limit=40)
        # config.today = date(year=2021, month=1, day=1)
        # self.fm.load_config = Mock(return_value=config)

    def tearDown(self):
        pass

    @property
    def model_class(self) -> AbstractModel:
        raise NotImplementedError()

    def files_to_return(self, files):
        self.fm.get_cards_map = Mock(return_value=files)

    def now_to_return(self, year=2026, month=1, day=1, hour=0, minute=0, second=0):
        datetime_value = datetime(year, month, day, hour, minute, second)
        self.tm.get_datetime = Mock(return_value=datetime_value)


__all__ = ["ModelTestCase"]
