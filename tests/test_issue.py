import unittest
import mock
from subprocess import DEVNULL, CalledProcessError as ProcessError
from requests.exceptions import Timeout

from mgit import issue

BASE_BRANCHE = "my_base_branch"

# TODO: Add descriptions for each function.
class IssueTestCase(unittest.TestCase):
    @mock.patch("mgit.issue.requests")
    def test_get_from_tracker(self, mock_requests):
        # Create a new Mock to imitate a Response
        mock_response = mock.Mock(
            **{"status_code": 200, "json.return_value": {"title": "update readme file"}}
        )

        # Test that the first request raises a Timeout
        mock_requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            issue.get_from_tracker("JIR-123")

        # Test alphanumeric ID
        mock_requests.get.side_effect = [mock_response]
        record = issue.get_from_tracker("JIR-123")
        self.assertEqual(record.id, "JIR-123")
        self.assertEqual(record.title, "Update Readme File")
        self.assertEqual(str(record), "JIR-123: Update Readme File")

        # Test numeric ID
        mock_requests.get.side_effect = [mock_response]
        record = issue.get_from_tracker("123")
        self.assertEqual(record.id, "123")
        self.assertEqual(record.title, "Update Readme File")
        self.assertEqual(str(record), "123: Update Readme File")

    def test_get_from_branch(self):
        # Test alphanumeric ID
        record = issue.get_from_branch("jir-123-update-readme-file")
        self.assertEqual(record.id, "JIR-123")
        self.assertEqual(record.title, "Update Readme File")
        self.assertEqual(str(record), "JIR-123: Update Readme File")

        # Test numeric ID
        record = issue.get_from_branch("123-update-readme-file")
        self.assertEqual(record.id, "123")
        self.assertEqual(record.title, "Update Readme File")
        self.assertEqual(str(record), "123: Update Readme File")
