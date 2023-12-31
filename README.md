# RenaBot v0.1

![RenaBot Logo](https://64.media.tumblr.com/3187c397dcfb358d519e08c2d1d1dc0e/b87b3de4b1fdc93c-88/s540x810/cd31af08d128130a28bf7af87c4ea9c34acd2daf.gif)

RenaBot is a customizable Discord bot created to help users set up their own bots without extensive programming knowledge. It provides an easy-to-use setup process that requires the bot token and user ID, allowing users to get their bot up and running quickly. The bot is designed to log data using a database and offers two initial functionalities: server information logging and a simple greeting response.

## File Structure

Here's the file structure of the RenaBot project:

```
RenaBot/
│-- RenaChan/
│   │-- cogs
│   	│-- __init__.py
│   	│-- cmds.py
│   	│-- tasks.py
│   │-- managers/
│   	│-- database.py
│   	│-- models.py
│   │-- tools/
│   	│-- __init__.py
│   	│-- session.py
│   │-- __init__.py
│   │-- session.py
│   │-- config.py
│   │-- dev.db
│   │-- events.py
│   │-- messages.py
│   │-- setup.py
│-- renachan.py
│-- .env
│-- file_structure.txt
│-- README.md
│-- generate_glossary.py
```

## Technology Used

Python | GitHub API | SQL Alchemy | Discord.py | Discord API

## Wiki Links

- [Database Schema](https://github.com/renahime/RenaChan.py/wiki/Database-Schema)
- [generate_glossary.py](https://github.com/renahime/RenaChan.py/wiki/generate_glossary.py)

## Activating Virtual Environment

To ensure a clean and isolated environment for RenaBot's dependencies, it's recommended to set up a virtual environment. Below are the steps to create and activate a virtual environment on different operating systems:

### Windows:

- [Python Official Website](https://www.python.org/downloads/): Download the latest version of Python for Windows. During installation, make sure to check the "Add Python to PATH" option.

- [Creating a Virtual Environment (venv) - Python Docs](https://docs.python.org/3/library/venv.html): Official documentation on creating virtual environments using `venv`.

### macOS and Linux:

- [Installing Python on macOS](https://docs.python-guide.org/starting/install3/osx/): A guide on installing Python on macOS.

- [Installing Python on Linux](https://docs.python-guide.org/starting/install3/linux/): A guide on installing Python on Linux.

- [Creating a Virtual Environment (venv) - Python Docs](https://docs.python.org/3/library/venv.html): Official documentation on creating virtual environments using `venv`.

Once the virtual environment is activated, you can install RenaBot's required dependencies without affecting other projects or your system-wide Python installation. Remember to activate the virtual environment whenever you work on RenaBot to ensure consistency and avoid potential conflicts.

## Getting Started

To set up RenaBot for your Discord server, follow these steps:

1. **Obtaining the Bot Token and User ID**

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
   - Navigate to the "Bot" tab in your application, click "Add Bot," and confirm the action.
   - Under the "Token" section, click "Copy" to copy the bot token to your clipboard. This token will be used during the setup process.
   - To obtain your user ID, enable Developer Mode in Discord's settings (User Settings > Advanced > Developer Mode).
   - Right-click on your username or nickname, and select "Copy ID" from the context menu. This will copy your user ID to the clipboard.

2. **Installing RenaChan.py**

   - First, clone the RenaBot repository to your local machine:
     ```
      git clone https://github.com/renahime/RenaBot.git
      cd RenaBot
     ```

3. **Installing Dependencies in Virtual Environment**

   - Ensure you have Python 3.9 or later installed on your system. If you don't have pipenv installed, you can install it using pip:
     ```
      pip install pipenv
     ```
   - Ensure you have Python 3.9 or later installed on your system. If you don't have pipenv installed, you can install it using pip:
     ```
      pipenv install requirements.txt
     ```

4. **Starting Virtual Enviorment**

   - Ensure you have Python 3.9 or later installed on your system.
   - Navigate to the RenaBot directory and install the required Python packages by running the following command:
     ```
     pipenv shell
     ```

5. **Starting RenaBot**
   - Run the `renachan.py` script to start RenaBot:
     ```
     python renachan.py
     ```
   - Upon first run, RenaBot will prompt you for the bot token and user ID required for setup.
   - RenaBot will create a `.env` file in the root directory and store the provided information for future use.
   - If you encounter any issues during setup, refer to the `.env.example` file in the root directory for guidance.

## Current Functionalities

1. **Server Information Logging**

   - RenaBot logs the following information when it joins a new server:
     - Channels
     - Members
     - Server information
   - Additionally, RenaBot sends a welcome message to the server upon joining.

2. **Greeting Response**
   - When you use the preferred command prefix, RenaBot will respond with a friendly greeting ("hello" in this version).

### Current Known Issues and Errors

1. **Database Deletion on Restart**

   - There is a known issue where the database (`dev.db`) will be deleted upon restarting RenaBot. This happens when the `CONFIG_VERSION` environment variable does not match the one stored in the `renachan` package. As a result, RenaBot will run the setup process again, which includes dropping and recreating the database tables. This will lead to the loss of existing data in the database.

Please note that RenaBot is a work in progress (WIP), and these issues will be addressed in future versions. If you encounter any other errors or have suggestions for improvements, please feel free to report them or contribute to the project. Your feedback is valuable in making RenaBot better! Happy botting! 😊

## Future Implementations

The following features are planned for future versions of RenaBot:

- Database retainment so that the database doesn't delete upon closing the application.
- Database migration support for updating the database structure without losing existing data.
- Database Flexibility: The ability to choose between using a local database such as SQLite or a more robust database system like MySQL, depending on your needs and preferences.
- A todo list feature that will remind users of upcoming tasks and keep track of task completion.
- A "harass" feature that can send notifications or messages to specific users for important communications.
- A study session feature that will track the times you study and give data analyitics.
- Data collection and machine learning capabilities to provide personalized recommendations (e.g., fashion recommendations).

## Contributing

Contributions to RenaBot are welcome! If you have ideas, bug fixes, or new features to propose, please feel free to open an issue or submit a pull request.

---

Please note that RenaBot is currently in version v0.1, and it is an ongoing project. As the development progresses, new functionalities and improvements will be added. Be sure to check back for updates and enjoy customizing your Discord bot with RenaBot! If you have any questions or need assistance, feel free to reach out to me on discord _tsuntsundere_ Happy botting! 😊
