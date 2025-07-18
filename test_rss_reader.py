"""
This module contains tests of unit tests ))
"""

import unittest
from unittest.mock import MagicMock, patch, call
from data_storage import save_as_json


class TestSaveAsJson(unittest.TestCase):

    @patch("builtins.open", new_callable=unittest.mock.mock_open)  # mocks built-in open func
    @patch("json.dump")  # mocks json.dump function and sends it to test func as 1st pos arg (as decor)
    def test_save_as_json(self, mock_json_dump, mock_open):
        mock_data = {
            "http://example.com/news1": MagicMock(
                json=MagicMock(return_value={"title": "News 1", "date": "01.01.2000"})
            ),
            "http://example.com/news2": MagicMock(
                json=MagicMock(return_value={"title": "News 2", "date": "02.02.2000"})
            ),
        }
        mock_logger = MagicMock()

        save_as_json(mock_data, mock_logger)

        expected_json_data = {
            "http://example.com/news1": {"title": "News 1", "date": "01.01.2000"},
            "http://example.com/news2": {"title": "News 2", "date": "02.02.2000"},
        }

        # arguments must correspond to the actual function !!!
        # Sequence of mock functions matters! mock open is called 2nd time in json_dump
        mock_open.assert_called_once_with("rss_feed.json", "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(expected_json_data, mock_open(), ensure_ascii=False, indent=4)
        mock_logger.info.assert_has_calls([call("Creating a JSON file..."), call("JSON file created")])


if __name__ == "__main__":
    unittest.main()
