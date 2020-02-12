# mgit

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Virtual environment setup](#virtual-environment-setup)
    - [standard](#standard)
    - [virtualenvwrapper](#virtualenvwrapper)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Code of Conduct](#code-of-conduct)

Run Git work flows for GitHub with issue tracking ticket numbers from issue tracking services like Jira.

Sample output from running the `mgit --help` command:

```
$ mgit --help
Usage: mgit [OPTIONS] COMMAND [ARGS]...

  Run Git work flows for GitHub with issue tracking ticket numbers.

Options:
  -l, --log-file FILENAME  File to log errors and warnings.  [default:
                           (stderr)]
  -v, --verbose            Enable verbose mode.
  --version                Show the version and exit.
  -h, --help               Show this message and exit.

Commands:
  branch        Create a branch using issue ID and title.
  commit        Create a commit and push to GitHub.
  open          Open an issue in the Google Chrome browser.
  pr            Alias for pull-request.
  pull-request  Create a GitHub Pull Request for the specified branch.
```

Sample output from running the `mgit branch --help` command:

```
$ mgit branch --help
Usage: mgit branch [OPTIONS] ISSUE_ID

  Create a branch using issue ID and title.

  The new branch name is taken from the title of the issue found. The new
  branch is created off of the --base-branch or the default base branch.

  NOTE
      User confirmation is required before the branch is created.

  EXAMPLES
      $ mgit branch JIR-123
      $ mgit branch JIR-123 --base-branch develop

Options:
  -b, --base-branch TEXT  The base branch to perform this action on.
  -h, --help              Show this message and exit.
```

## Installation

**Warning:** This installation method is temporary until the best distribution
method is determined.

1. `git clone git@github.com:greganswer/mgit.git`
1. `cd mgit`
1. `pip3 install .`

## Usage

```bash
# Assuming you have a Jira ticket with the following info:
#       ID: JIR-642
#       Title: Update README file
mgit branch JIR-642
#=> jir-642-update-readme-file

mgit commit
#=> Message: JIR-642: Update Readme File

# If you make changes and run it again, it will make another commit with the
# same name
mgit commit
#=> Message: JIR-642: Update Readme File

mgit pull-request
#=> Title: JIR-642: Update Readme File

mgit tag
#=> Tag Title: my_project v2.1.7
```

## Development

### Virtual environment setup

Make sure you have [Python 3.7.4](https://www.python.org/downloads) installed.

There are 2 ways to set this up for development: standard vs. `virtualenvwrapper`.
The `virtualenvwrapper` package requires a one time setup per machine but it's a bit
easier to use day-to-day.

#### standard

```bash
# Install packages locally
pip3 install --editable .

# Install **virtualenv** using pip3
pip3 install virtualenv

# Create a virtual environment. **NOTE:** You can use any name instead of **venv**.
python3 -m venv env

# Activate your virtual environment:
source venv/bin/activate
```

If you need to deactivate:

    deactivate

#### virtualenvwrapper

If you prefer to use `virtualenvwrapper` do the following:

1. Install **virtualenvwrapper** using pip3

        pip3 install virtualenvwrapper

1. Add the following to `~/.bash_profile` or `~/.zshrc`:

        export WORKON_HOME=$HOME/code/.virtualenvs
        export PROJECT_HOME=$HOME/code
        export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python
        export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
        export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
        source /usr/local/bin/virtualenvwrapper.sh

1. Update the current shell with `source ~/.bash_profile` or `source ~/.zshrc`
1. Make the virtual environment

        mkvirtualenv mgit

1. Enter the project environment

        workon mgit

Refer to [this Stack Overflow](https://stackoverflow.com/a/25583193)
for more info.

## Testing

First install the [Python Click package](https://click.palletsprojects.com/en/7.x/) globally

To run tests, execute the following command from the root directory:

    bin/test
  
To automatically run tests after updating files:

    bin/test watch

For more info run:

    bin/test --help

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/greganswer/mgit.
This project is intended to be a safe, welcoming space for collaboration, and
contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org)
code of conduct.

## License

The project is available as open source under the terms of the
[MIT License](https://opensource.org/licenses/MIT).

## Code of Conduct

Everyone interacting in this project’s codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](/CODE_OF_CONDUCT.md).
