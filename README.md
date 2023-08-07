# API WatchBot

[![Lint](https://github.com/josehenriqueroveda/watchbot/actions/workflows/black.yml/badge.svg)](https://github.com/josehenriqueroveda/watchbot/actions/workflows/black.yml)
[![Bandit](https://github.com/josehenriqueroveda/watchbot/actions/workflows/bandit.yml/badge.svg)](https://github.com/josehenriqueroveda/watchbot/actions/workflows/bandit.yml)


API WatchBot is a Python-based Telegram bot that monitors the status of multiple APIs and sends notifications to a Telegram group if any of them go down.
It allows the user to check the status of the APIs by sending a command to the bot too.

## Installation

1. Clone the repository to your local machine.
2. Install [Poetry](https://python-poetry.org/docs/#installation) if you haven't already.
3. In the project directory, run `poetry install` to install the required dependencies.
4. Set up a Telegram bot and obtain a bot token.
5. Set up a Telegram group and obtain the group ID.
6. Set up environment variables for the bot token, group ID, and API URLs and names.
7. Run the bot using `poetry run python main.py`.

## Usage

The bot can be used to check the status of APIs by sending the `/status` command to the bot. The bot will respond with the status of each API, indicating whether it is up or down.
It also runs in the background and monitors the APIs. If any of them go down, it will send a notification to the Telegram group.

## Example

<img src="https://raw.githubusercontent.com/josehenriqueroveda/watchbot/main/examples/watchbot-telegram.png" width=480 class="inline"/>

## Contributing

Contributions to the project are welcome. To contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
