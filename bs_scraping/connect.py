from mongoengine import connect
import configparser
import pathlib

file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

mongo_user = config.get('DB_DEV_BS4', 'user')
mongodb_pass = config.get('DB_DEV_BS4', 'PASSWORD')
db_name = config.get('DB_DEV_BS4', 'db_name')
domain = config.get('DB_DEV_BS4', 'domain')

# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)
