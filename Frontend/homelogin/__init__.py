fname = "valuesTest.txt"
featuresText = "features.txt"
d = dict()
features = {"admin": [],
            "user": []
            }
with open(fname) as f:
    for line in f:
        parsed = line.split(" ")
        d[parsed[0]] = parsed[1].rsplit()[0]

with open(featuresText) as f:
    for line in f:
        parsed = line.split(":")
        print parsed
        if parsed[2][:-1] == "True":
            features["admin"].append({
                "command": parsed[0],
                "description": parsed[1]
            })
        else:
            features["user"].append({
                "command": parsed[0],
                "description": parsed[1]
            })
