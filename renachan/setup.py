import time

import renachan
def __init__():
    input_local_host = "127.0.0.5000"
    input_local_port = "5000"
    input_db_schema = "renachan"
    input_user = "rena"

    input_bot_token = input("Discord bot token: ")
    input_bot_prefix = input("Command Prefix: ")
    input_bot_status = input("Bot status: (Playing xxx) ")

    try:
        config = f"""CONFIG_VERSION={renachan.config_version()}
BOT_TOKEN={input_bot_token}
BOT_PREFIX={input_bot_prefix}
BOT_STATUS={input_bot_status}
"""
        open('./.env', 'w').write(config)
        print("\n[*] Successfully created .env file!")
        print("rena_chan.py setup complete! Starting bot in 5 seconds...")
        time.sleep(5)
    except Exception as e:
        print("\n[!] An error occurred when creating config file.\n" + str(e))
        quit()
