import time
import logging

import renachan
def __init__():
    input_local_host = "127.0.0.5000"
    input_local_port = "5000"
    input_db_schema = "renachan"
    input_user = "rena"
    database_url = "sqlite:///dev.db"

    input_bot_token = input("Discord bot token: ")
    input_bot_owner = input("Discord user ID:")
    input_bot_prefix = input("Command Prefix: ")
    input_bot_status = input("Bot status: (Playing xxx) ")
    input_storage_type = input("Do you have SQLITE? [Y/N] ")
    if input_storage_type.lower() == "y" or input_storage_type.lower() == "yes":
        input_storage_type = "sqlite"
    else:
        logging.error("ERROR: Sorry this bot only works on local databases, stay updated on this feature by following me on Twitter @renadotdev :)")
        return

    try:
        config = f"""CONFIG_VERSION={renachan.config_version()}
BOT_TOKEN={input_bot_token}
BOT_OWNER={input_bot_owner}
BOT_PREFIX={input_bot_prefix}
BOT_STATUS={input_bot_status}
STORAGE_TYPE={input_storage_type}

DB_HOST={input_local_host}
DB_PORT={input_local_port}
DB_SCHEMA={input_db_schema}
DB_USER={input_user}
DATABASE_URL={database_url}
"""
        open('./.env', 'w').write(config)
        logging.info("\n[*] Successfully created .env file!")
        logging.info("rena_chan.py setup complete! Starting bot in 5 seconds...")
        time.sleep(5)
    except Exception as e:
        logging.info("\n[!] An error occurred when creating config file.\n" + str(e))
        quit()
