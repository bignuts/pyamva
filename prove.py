from dotenv.main import dotenv_values, load_dotenv


env1 = load_dotenv(verbose=True)
print(env1)
env2 = dotenv_values(".env")
print(env2['MT5_USER'])