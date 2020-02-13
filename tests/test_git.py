import unittest
import mock
from subprocess import CalledProcessError as ProcessError
from subprocess import DEVNULL

from mgit import git

BASE_BRANCHE = "my_base_branch"

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
        self.assertEqual("my_branch_name", git.current_branch())
        args = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        mock_check_output.assert_called_with(args)

    @mock.patch("mgit.git.subprocess.check_call")
    def test_branch_exists_true(self, mock_check_call):
        self.assertTrue(git.branch_exists(BASE_BRANCHE))
        args = ["git", "rev-parse", "--quiet", "--verify", BASE_BRANCHE]
        mock_check_call.assert_called_with(args, stdout=DEVNULL)

    @mock.patch("mgit.git.subprocess.check_call")
    def test_branch_exists_false(self, mock_check_call):
        args = ["git", "rev-parse", "--quiet", "--verify", BASE_BRANCHE]
        mock_check_call.side_effect = ProcessError(returncode=17, cmd="".join(args))
        self.assertFalse(git.branch_exists(BASE_BRANCHE))
        mock_check_call.assert_called_with(args, stdout=DEVNULL)

    @mock.patch("mgit.git.branch_exists")
    def test_default_base_branch(self, mock_branch_exists):
        branches = ["dev", "develop", "development", "master"]
        self.assertEqual(branches, git.DEFAULT_BASE_BRANCHES)
        for branch in git.DEFAULT_BASE_BRANCHES:

            def side_effect(arg):
                return True if arg == branch else False

            mock_branch_exists.side_effect = side_effect
            self.assertEqual(branch, git.default_base_branch())

    @mock.patch("mgit.git.subprocess.call")
    def test_new_branch_off(self, mock_call):
        new_branch = "my_new_branch"
        git.new_branch_off(BASE_BRANCHE, new_branch)
        mock_call.assert_has_calls(
            [
                mock.call(["git", "checkout", BASE_BRANCHE]),
                mock.call(["git", "pull"]),
                mock.call(["git", "checkout", "-b", new_branch]),
            ]
        )

    @mock.patch("mgit.git.subprocess.call")
    def test_commit_all(self, mock_call):
        message = "Add new files"
        git.commit_all(message)
        mock_call.assert_has_calls(
            [
                mock.call(["git", "add", "."], shell=False),
                mock.call(f'git commit -m "{message}"', shell=True),
            ]
        )

    @mock.patch("mgit.git.subprocess.call")
    def test_push(self, mock_call):
        git.push(BASE_BRANCHE)
        mock_call.assert_has_calls(
            [
                mock.call(["git", "push", "-f"], shell=False),
                mock.call(
                    ["git", "push", "--set-upstream", "origin", BASE_BRANCHE],
                    shell=False,
                ),
            ]
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()
