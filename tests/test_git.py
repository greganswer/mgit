import unittest
import mock
import subprocess

from mgit import git


class GitTestCase(unittest.TestCase):
    @mock.patch("mgit.git.subprocess.check_output")
    def test_current_branch(self, mock_check_output):
        mock_check_output.return_value = b"my_branch_name"

        actual = git.current_branch()

        args = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        mock_check_output.assert_called_with(args)
        self.assertEqual("my_branch_name", actual)

    # @mock.patch("mgit.git.subprocess.check_call")
    # def test_branch_exists(self, mock_check_call):
    #     mock_check_call.side_effect = subprocess.CalledProcessError
    #     with self.assertRaises(subprocess.CalledProcessError):
    #         branch = "fake_branch"
    #         actual = git.branch_exists(branch)
    #         args = ["git", "rev-parse", "--quiet", "--verify", branch]
    #         mock_check_call.assert_called_once()
    #         self.assertFalse(actual)

    #     branch = "master"
    #     actual = git.branch_exists(branch)
    #     args = ["git", "rev-parse", "--quiet", "--verify", branch]
    #     # mock_check_call.assert_called_with(
    #     #     args, stdout=subprocess.DEVNULL
    #     # )
    #     self.assertTrue(actual)


# Run the tests
if __name__ == "__main__":
    unittest.main()
