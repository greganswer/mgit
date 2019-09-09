# mgit

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Virtual environment](#virtual-environment)
    - [virtualenvwrapper](#virtualenvwrapper)
- [Contributing](#contributing)
- [License](#license)
- [Code of Conduct](#code-of-conduct)

Run Git work flows for GitHub with issue tracking ticket numbers from issue tracking services like Jira.

## Installation

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

### Virtual environment

1. Install [Python 3.7.4](https://www.python.org/downloads)

1. Install packages locally

        pip3 install --editable .

1. Install **virtualenv** using pip3

        pip3 install virtualenv

1. Create a virtual environment. **NOTE:** You can use any name instead of **venv**.

        python3 -m venv env

1. Active your virtual environment:

        source venv/bin/activate

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


Refer to [this Stack Overflow](https://stackoverflow.com/a/25583193)
for more info.

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
