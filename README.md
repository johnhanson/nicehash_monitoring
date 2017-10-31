# nicehash_monitoring
Uses nicehash's API to monitor various stats, both public and private.


Logs the current global stats from `?method=stats.global.current` every minute to a csv file.

TODO: add personal information about your hashing rate to other logs.

Known Bugs:

 - Sometimes nicehash returns a 520: Origin Error for some unknown reason, which throws an uncaught exception and quits the program. Need to detect and handle it (normally, just retrying one or two more times fixes it)
