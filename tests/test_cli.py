"""
References:
- https://www.toptal.com/python/an-introduction-to-mocking-in-python
- https://realpython.com/python-mock-library
- https://click.palletsprojects.com/en/7.x/testing/
"""
import unittest
import mock
from click.testing import CliRunner
from requests.exceptions import Timeout, HTTPError
from subprocess import DEVNULL, CalledProcessError as ProcessError

from mgit.cli import cli

BASE_BRANCH = "my_base_branch"
NEW_BRANCH = "jir-472-update-readme-file"
ISSUE_ID = "JIR-472"
ISSUE_TITLE = "JIR-472: Update Readme File"
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
        mock_requests.get.return_value = mock_response
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
        mock_requests.get.return_value = mock_response
        result = self.runner.invoke(
            cli, ["branch", ISSUE_ID, "--base-branch", BASE_BRANCH], input="yes"
        )

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

    @mock.patch("mgit.app.git")
    def test_commit(self, mock_git):
        mock_git.current_branch.return_value = NEW_BRANCH

        result = self.runner.invoke(cli, ["commit"], input="yes")

        self.assertIn(
            "Create a commit with the message", result.output, msg=result.exception
        )
        self.assertIn("Update Readme File", result.output, msg=result.exception)
        self.assertEqual(0, result.exit_code)
        mock_git.commit_all.assert_called_with(f"{ISSUE_TITLE}\n\nCloses #JIR-472")
        mock_git.push.assert_called_with(NEW_BRANCH)

    @mock.patch("mgit.app.git")
    def test_commit_with_message(self, mock_git):
        mock_git.current_branch.return_value = NEW_BRANCH
        message = "My new commit message"

        result = self.runner.invoke(cli, ["commit", "-m", message], input="yes")

        self.assertIn(
            "Create a commit with the message", result.output, msg=result.exception
        )
        self.assertIn(message, result.output, msg=result.exception)
        self.assertEqual(0, result.exit_code)
        mock_git.commit_all.assert_called_with(message)
        mock_git.push.assert_called_with(NEW_BRANCH)

    @mock.patch("mgit.app.git")
    @mock.patch("mgit.issues.requests")
    def test_commit_with_issue_id(self, mock_requests, mock_git):
        mock_git.current_branch.return_value = NEW_BRANCH

        # Create a new Mock to imitate a Response
        mock_response = mock.Mock(
            **{"status_code": 200, "json.return_value": {"title": "update readme file"}}
        )

        # Test successful HTTP request
        mock_requests.get.return_value = mock_response
        result = self.runner.invoke(
            cli, ["commit", "--issue-id", ISSUE_ID], input="yes"
        )

        self.assertIn(
            "Create a commit with the message", result.output, msg=result.exception
        )
        self.assertIn(ISSUE_TITLE, result.output, msg=result.exception)
        self.assertEqual(0, result.exit_code)
        mock_git.commit_all.assert_called_with(f"{ISSUE_TITLE}\n\nCloses #JIR-472")
        mock_git.push.assert_called_with(NEW_BRANCH)

    @mock.patch("mgit.issues.requests")
    def test_commit_exceptions(self, mock_requests):
        # Test output with request Timeout
        mock_requests.get.side_effect = REQUEST_TIMEOUT
        result = self.runner.invoke(
            cli, ["commit", "--issue-id", ISSUE_ID], input="yes"
        )
        self.assertIn(str(REQUEST_TIMEOUT), result.output, msg=result.exception)
        self.assertEqual(1, result.exit_code)

        # Test output with request HTTPError
        mock_requests.get.side_effect = REQUEST_HTTP_ERROR
        result = self.runner.invoke(
            cli, ["commit", "--issue-id", ISSUE_ID], input="yes"
        )
        self.assertIn(str(REQUEST_HTTP_ERROR), result.output, msg=result.exception)
        self.assertEqual(1, result.exit_code)

    def test_open(self):
        pass

    def test_pull_request(self):
        pass


# Run the tests
if __name__ == "__main__":
    unittest.main()
