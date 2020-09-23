"""
Enviroment Manage
"""

# Libraries
import environ

env = environ.Env()

URL_ENV = env.path(
    'ENV_FILE_PATH',
    default=(environ.Path(__file__) - 2).path('.env')()
)()

env.read_env(URL_ENV)
