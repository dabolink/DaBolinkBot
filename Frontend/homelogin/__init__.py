fname = "valuesLive.txt"
d = dict()
with open(fname) as f:
    for line in f:
        parsed = line.split(" ")
        d[parsed[0]] = parsed[1].rsplit()[0]
