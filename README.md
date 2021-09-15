[![Heroku deployment Status](https://github.com/tikerlade/Python-Template/workflows/Heroku%20deploy/badge.svg)](https://python-template-application.herokuapp.com/)
[![Python checks Status](https://github.com/tikerlade/Python-Template/workflows/Python%20checks/badge.svg)](https://github.com/tikerlade/Python-Template/actions/)

# Python :snake: template project
This project have everything I need to start a Python project :pencil:.

This includes but not limits: linters, tests + coverage, .gitignore, CI setting up. Below you can see instructions what you need to configure for your personal application + full list of technologies pre-configured with links :link:.

## Instructions :bookmark_tabs:
_If you are on a Unix system you can run `./setup.sh` to skip all next steps._

- `pip install -r requirements.txt` (this will download all important libraries)
- `pre-commit intall` (this will enable pre-commit checks)

## GitHub repository setup :octocat:
### Heroku deployment :arrow_up:
If you want app from your `app/` folder to be deployed to Heroku do the following:

- Go to your GitHub repository page `Settings`
- In the left menu at the bottom choose `Secrets`
- Add the following variables:
    - `EMAIL` - email which you are registered at Heroku with
    - `HEROKU_APP` - name of your heroku app
    - `HEROKU_API_KEY` - key from your [account page](https://dashboard.heroku.com/account)

### GitHub actions badges :tm:
If you want to add badges about GitHub actions that have been passed / failed to your README.md add to the top of README the following:
```markdown
[![Invisible-text](https://github.com/your_username/repository_name/workflows/workflow_name/badge.svg)](https://github.com/your_username/repository_name/actions/)
```

- `Invisible-text` - replacement text when badge cannot be loaded
- `your_username` - your GitHub username or organization name (where repository is located)
- `repository_name` - name of repository where GitHub actions will be executed
- `workflow_name` - name of workflow (basically first line from `github/workflows/___.yml` file), spaces should be replaced with `%20`


## Structure
- `app/` - contains full code to deploy to [Heroku](https://www.heroku.com/)
- `python-template/` - main part of your Python code should be placed here
- `.gitignore` - files and folders that won't be tracked by git
- `.pre-commit-config.yaml` - file with checks that pre-commit needs to run
- `README.md` - this file with explanations
- `requirements.txt` - file with Python requirements for proper work
- `setup.cfg` - configuration of tools which will be used in pre-commit and other tools installed from requirements.txt

## Technologies :floppy_disk:
- Heroku
- GitHub Actions CI
- pre-commit
  - mypy
  - flake8
  - pytest
  - isort
