import os
import renachan
from dotenv import load_dotenv

load_dotenv()


def bot_owner():
    return eval(os.getenv('BOT_OWNER', "216127021028212737"))


def bot_token():
    return os.getenv('BOT_TOKEN')


def bot_prefix():
    return os.getenv('BOT_PREFIX', '!rena ')

def set_project_folder_as_env_variable():
    project_folder = os.getcwd()
    os.environ["RENA_PROJECT_FOLDER"] = project_folder


def bot_status():
    default_prefix = f'{", ".join(renachan.config.bot_prefix())} | RenaChan.py {renachan.version()}'
    try:
        return eval(os.getenv('BOT_STATUS', default_prefix))
    except:
        return os.getenv('BOT_STATUS', default_prefix)

def db_host():
    return os.environ['DB_HOST']

def storage_type():
    return os.environ['STORAGE_TYPE']


def db_port():
    return os.getenv('DB_PORT', "5000")

def db_schema():
    return os.environ['DB_SCHEMA']

def db_user():
    return os.environ['DB_USER']
