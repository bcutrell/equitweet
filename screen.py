import sys

i = 1
sys.stdout.write("\rDoing thing %i" % i)
i = 2
sys.stdout.flush()


https://stackoverflow.com/questions/18421757/live-output-from-subprocess-command
