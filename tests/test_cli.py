import unittest
import mock
from click.testing import CliRunner
from requests.exceptions import Timeout, HTTPError
from subprocess import DEVNULL, CalledProcessError as ProcessError

from mgit.cli import cli

BASE_BRANCH = "my_base_branch"
NEW_BRANCH = "jir-472-update-readme-file"
ISSUE_ID = "JIR-472"
REQUEST_TIMEOUT = Timeout("HTTP Request Timeout")
REQUEST_HTTP_ERROR = HTTPError("HTTP Request Error")


class GitTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli(self):
        result = self.runner.invoke(cli)
        self.assertIn("Usage: mgit [OPTIONS] COMMAND [ARGS]...", result.output)
        self.assertEqual(0, result.exit_code)

    @mock.patch("mgit.git.create_branch")
    @mock.patch("mgit.issues.requests")
    def test_branch(self, mock_requests, mock_create_branch):
        # Create a new Mock to imitate a Response
        mock_response = mock.Mock(
            **{"status_code": 200, "json.return_value": {"title": "update readme file"}}
        )

        # Test successful HTTP request
        mock_requests.get.side_effect = [mock_response]
        result = self.runner.invoke(cli, ["branch", ISSUE_ID], input="yes")

        expected = f"This will create a branch off master named {NEW_BRANCH}"
        self.assertIn(expected, result.output, msg=result.exception)
        self.assertEqual(0, result.exit_code)
        mock_create_branch.assert_called_with("master", NEW_BRANCH)

    @mock.patch("mgit.git.create_branch")
    @mock.patch("mgit.issues.requests")
    def test_branch_with_base_branch(self, mock_requests, mock_create_branch):
        # Create a new Mock to imitate a Response
        mock_response = mock.Mock(
            **{"status_code": 200, "json.return_value": {"title": "update readme file"}}
        )

        # Test successful HTTP request
        mock_requests.get.side_effect = [mock_response]
        command = ["branch", ISSUE_ID, "--base-branch", BASE_BRANCH]
        result = self.runner.invoke(cli, command, input="yes")

        expected = f"This will create a branch off {BASE_BRANCH} named {NEW_BRANCH}"
        self.assertIn(expected, result.output, msg=result.exception)
        self.assertEqual(0, result.exit_code)
        mock_create_branch.assert_called_with(BASE_BRANCH, NEW_BRANCH)

    def test_branch_missing_issue_id(self):
        result = self.runner.invoke(cli, ["branch"])
        expected = 'Error: Missing argument "ISSUE_ID"'
        self.assertIn(expected, result.output, msg=result.exception)
        self.assertEqual(2, result.exit_code)

    @mock.patch("mgit.issues.requests")
    def test_branch_exceptions(self, mock_requests):
        # Test output with request Timeout
        mock_requests.get.side_effect = REQUEST_TIMEOUT
        result = self.runner.invoke(cli, ["branch", ISSUE_ID])
        self.assertIn(str(REQUEST_TIMEOUT), result.output, msg=result.exception)
        self.assertEqual(1, result.exit_code)

        # Test output with request HTTPError
        mock_requests.get.side_effect = REQUEST_HTTP_ERROR
        result = self.runner.invoke(cli, ["branch", ISSUE_ID])
        self.assertIn(str(REQUEST_HTTP_ERROR), result.output, msg=result.exception)
        self.assertEqual(1, result.exit_code)


# Run the tests
if __name__ == "__main__":
    unittest.main()
