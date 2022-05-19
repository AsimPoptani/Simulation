MILLISECONDS_IN_SECOND = 1000
MILLISECONDS_IN_MINUTE = 60 * MILLISECONDS_IN_SECOND
MILLISECONDS_IN_HOUR = 60 * MILLISECONDS_IN_MINUTE
MILLISECONDS_IN_DAY = 24 * MILLISECONDS_IN_HOUR

NANOSECONDS_IN_MILLISECOND = 1000000
NANOSECONDS_IN_SECOND = MILLISECONDS_IN_SECOND * NANOSECONDS_IN_MILLISECOND
NANOSECONDS_IN_MINUTE = 60 * NANOSECONDS_IN_SECOND
NANOSECONDS_IN_HOUR = 60 * NANOSECONDS_IN_MINUTE
NANOSECONDS_IN_DAY = 24 * NANOSECONDS_IN_HOUR

def nanosecond_string(nanoseconds):
    string = ''

    days = nanoseconds // NANOSECONDS_IN_DAY
    if days != 0:
        string += str(days) + " days "
        nanoseconds -= days * NANOSECONDS_IN_DAY

    hours = nanoseconds // NANOSECONDS_IN_HOUR
    if hours != 0:
        string += str(hours) + " hours "
        nanoseconds -= hours * NANOSECONDS_IN_HOUR

    minutes = nanoseconds // NANOSECONDS_IN_MINUTE
    if minutes != 0:
        string += str(minutes) + " minutes "
        nanoseconds -= minutes * NANOSECONDS_IN_MINUTE

    seconds = nanoseconds // NANOSECONDS_IN_SECOND
    if seconds != 0:
        string += str(seconds) + " seconds "
        nanoseconds -= seconds * NANOSECONDS_IN_SECOND

    if hours == 0 and minutes == 0 and seconds == 0:
        milliseconds = nanoseconds // NANOSECONDS_IN_MILLISECOND
        if milliseconds != 0:
            string += str(milliseconds) + " milliseconds "
            nanoseconds -= milliseconds * NANOSECONDS_IN_MILLISECOND
        elif nanoseconds != 0:
            string += str(nanoseconds) + " nanoseconds "

    return string
