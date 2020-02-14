import unittest
import mock
from subprocess import DEVNULL, CalledProcessError as ProcessError
from requests.exceptions import Timeout

from mgit import issues

BASE_BRANCHE = "my_base_branch"


class IssuesTestCase(unittest.TestCase):
    def test_issues_properties(self):
        record = issues.Issue("JIR-123", "update readme file")

        self.assertEqual(str(record), "JIR-123: Update Readme File")
        self.assertEqual(record.id, "JIR-123")
        self.assertEqual(record.branch_name, "jir-123-update-readme-file")
        self.assertEqual(record.title, "Update Readme File")

    def test_from_branch(self):
        # Test alphanumeric ID
        record = issues.from_branch("jir-123-update-readme-file")
        self.assertEqual(str(record), "JIR-123: Update Readme File")

        # Test numeric ID
        record = issues.from_branch("123-update-readme-file")
        self.assertEqual(str(record), "123: Update Readme File")

    @mock.patch("mgit.issues.requests")
    def test_from_tracker(self, mock_requests):
        # Create a new Mock to imitate a Response
        mock_response = mock.Mock(
            **{"status_code": 200, "json.return_value": {"title": "update readme file"}}
        )

        # Test that the first request raises a Timeout
        mock_requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            issues.from_tracker("JIR-123")

        # Test alphanumeric ID
        mock_requests.get.side_effect = [mock_response]
        record = issues.from_tracker("JIR-123")
        self.assertEqual(str(record), "JIR-123: Update Readme File")

        # Test numeric ID
        mock_requests.get.side_effect = [mock_response]
        record = issues.from_tracker("123")
        self.assertEqual(str(record), "123: Update Readme File")
