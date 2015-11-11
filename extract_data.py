import re

def extractTriples(fileName):
    data = []
    with open(fileName, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
            if l.startswith("#$#"):
                l = l.split("#$#")[1:]

                val = l[2]
                valTag = val[:4]
                vals = val[4:].split("#")

                for v in vals:
                    #print([l[0], l[1], valTag+v])
                    newValue = "\t".join([l[0], l[1], valTag+v])
                    data.append(newValue)

        with open(fileName+"_Triples", "w", encoding="utf8") as f9:
            f9.write("\n".join(data))
                
                #input(vals)

#extractData("Shamela_0023696")
extractTriples("Shamela_0023696")
print("Done!")
