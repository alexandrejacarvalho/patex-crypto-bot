import os

environment = os.environ.get("PROJECT_ENV")

if environment == "staging":
    print("Started using staging configuration.")
    from .staging import *
elif environment == "production":
    print("Started using production configuration.")
    from .production import *
elif environment == "test":
    print("Started using test configuration.")
    from .test import *
else:
    print("PROJECT_ENV environment variable not found. "
          "Using development configuration.")
    from .development import *