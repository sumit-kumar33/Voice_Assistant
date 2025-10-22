import datetime
def get_current_date():
    now = datetime.datetime.now()
    date_string = now.strftime("%B %d, %Y")
    day_name = now.strftime("%A")
    return (f"Today is {day_name}, {date_string}")