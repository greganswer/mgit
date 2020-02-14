import unittest
import mock
from subprocess import DEVNULL, CalledProcessError as ProcessError
from click.testing import CliRunner

from mgit.cli import cli

BASE_BRANCHE = "my_base_branch"
ISSUE_ID = "JIR-472"

# TODO: Add descriptions for each function.
class GitTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_cli(self):
        result = self.runner.invoke(cli)
        self.assertIn("Usage: mgit [OPTIONS] COMMAND [ARGS]...", result.output)
        self.assertEqual(0, result.exit_code)

    # @mock.patch("mgit.app.requests")
    # def test_branch(self, mock_request):
    #     result = self.runner.invoke(cli, ["branch", ISSUE_ID])
    #     if result.exception:
    #         print(result.exception)
    #     self.assertIsNone(result.exception)
    #     self.assertIn("Usage: mgit [OPTIONS] COMMAND [ARGS]...", result.output)
    #     self.assertEqual(0, result.exit_code)

    # def test_branch_without_default_base_branch(self):
    #     pass

    # def test_open(self):
    #     print(dir(cli))
    #     result = CliRunner().invoke(cli, ["open"])
    #     print(result.exc_info)
    #     print(result.exception)
    #     # self.assertIn("hello world", result.output)
    #     self.assertEqual(0, result.exit_code)


# Run the tests
if __name__ == "__main__":
    unittest.main()
