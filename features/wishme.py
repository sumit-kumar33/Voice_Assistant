import datetime
from config_files.config import Name
# Wishes Good Morning, Afternoon, Evening according to time
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        salutation = "Good Morning!"
    elif 12 <= hour < 18:
        salutation = "Good Afternoon!"
    else:
        salutation = "Good Evening!"
    return f"{salutation} I am {Name}. How may I help you today? You can speak *exit* anytime for me to exit."