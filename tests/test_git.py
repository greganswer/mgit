import unittest
import mock
from subprocess import CalledProcessError as ProcessError
from subprocess import DEVNULL

from mgit import git

# TODO: Add descriptions for each function.
class GitTestCase(unittest.TestCase):
    @mock.patch("mgit.git.os.path.isdir")
    def test_initialized(self, mock_isdir):
        mock_isdir.return_value = False
        self.assertFalse(git.initialized())
        mock_isdir.assert_called_with(".git")

        mock_isdir.return_value = True
        self.assertTrue(git.initialized())
        mock_isdir.assert_called_with(".git")

    @mock.patch("mgit.git.subprocess.check_output")
    def test_current_branch(self, mock_check_output):
        mock_check_output.return_value = b"my_branch_name"

        actual = git.current_branch()

        args = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        mock_check_output.assert_called_with(args)
        self.assertEqual("my_branch_name", actual)

    @mock.patch("mgit.git.subprocess.check_call")
    def test_branch_exists_true(self, mock_check_call):
        branch = "real_branch"
        actual = git.branch_exists(branch)

        args = ["git", "rev-parse", "--quiet", "--verify", branch]
        mock_check_call.assert_called_with(args, stdout=DEVNULL)
        self.assertTrue(actual)

    @mock.patch("mgit.git.subprocess.check_call")
    def test_branch_exists_false(self, mock_check_call):
        branch = "fake_branch"
        args = ["git", "rev-parse", "--quiet", "--verify", branch]
        cmd = "".join(args)
        mock_check_call.side_effect = ProcessError(returncode=17, cmd=cmd)
        actual = git.branch_exists(branch)

        mock_check_call.assert_called_with(args, stdout=DEVNULL)
        self.assertFalse(actual)

    @mock.patch("mgit.git.branch_exists")
    def test_default_base_branch(self, mock_branch_exists):
        branches = ["dev", "develop", "development", "master"]
        self.assertEqual(branches, git.DEFAULT_BASE_BRANCHES)
        for branch in git.DEFAULT_BASE_BRANCHES:

            def side_effect(arg):
                return True if arg == branch else False

            mock_branch_exists.side_effect = side_effect
            actual = git.default_base_branch()
            self.assertEqual(branch, actual)

    def test_commit(self):
        pass


# Run the tests
if __name__ == "__main__":
    unittest.main()
