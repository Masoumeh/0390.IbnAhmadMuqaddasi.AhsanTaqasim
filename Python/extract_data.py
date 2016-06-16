import re
# To extract hierarchical data in triples from a tagged text
# To include distances the 6th line should be changed
def extractTriples(fileName):
    data = []
    with open(fileName, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
            # to include distances in extraction, remove PROV and REG strings in the below line
            if l.startswith("#$#PROV") or l.startswith("#$#REG"):
                l = l.split("#$#")[1:]

                val = l[2]
                valTag = val[:4]
                vals = val[4:].split("#")

                for v in vals:
                    #print([l[0], l[1], valTag+v])
                    newValue = "\t".join([l[0], l[1], valTag+v])
                    data.append(newValue)

        with open("../Data/" + fileName + "_Triples", "w", encoding="utf8") as f9:
            f9.write("\n".join(data))


extractTriples("../Data/Shamela_0023696")
print("Done!")
