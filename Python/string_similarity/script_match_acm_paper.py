import py_stringmatching as ps
import get_sttl_reg as gsr
import numpy as np
import extract_cornu_names as ecn
import csv,os
import jellyfish as jf
import jellyfish._jellyfish as py_jellyfish
import io
from aratext import normalization as norm


muq_sttls = gsr.get_sttl("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all")
write_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/sample_matches"
muq_sttls = list(muq_sttls)
cornu_names = list(ecn.extract_cornu_names())
sttls = []
# sample_index = np.random.choice(1200, 200)
with open("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/sample_data", "r") as data:
    for line in data:
      # print(line)
      sttls.append(line)
# print(sttls)
c = ps.Cosine()
jac = ps.Jaccard()
jaro = ps.Jaro()
jaroW = ps.JaroWinkler()
lev = ps.Levenshtein()
# dam_lev = py_jellyfish.damerau_levenshtein_distance() # args
hamm = ps.HammingDistance()
# hamm_jelly = jf.hamming_distance() # args
mon_elk = ps.MongeElkan()
over_coeff = ps.OverlapCoefficient()
affine = ps.Affine()
cosine = ps.Cosine()
dice = ps.Dice()
needle = ps.NeedlemanWunsch()
smith = ps.SmithWaterman()
tfidf = ps.TfIdf()
soft = ps.SoftTfIdf()
gen_jaccard = ps.GeneralizedJaccard()

# score = smith.get_raw_score("test","tefstil")
# print(score)



file_exists = os.path.isfile(write_file)
with open(write_file, 'a', encoding="utf8") as matches_file:
    print(cosine.get_raw_score(["hello world"], ["hallo worldi"]))
    headers = ["Geo Title", "Cornu Title", "Method", "Score", "Status"]
    writer = csv.DictWriter(matches_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    if not file_exists:
        writer.writeheader()  # file doesn't exist yet, write a header
    for s in sttls:
        st = s.strip("\n")
        for cn in cornu_names:
            score_jaro = dice.get_raw_score(norm.normalize_alphabet(st).split(" "), norm.normalize_alphabet(cn).split(" "))
            score_jaro = score_jaro
            if score_jaro > 0.55:
                writer.writerow({"Geo Title": st, "Cornu Title": cn, "Method": "Dice 0.55", "Score": score_jaro,
                                 "Status": "NA"})
            # else:
            #     print(st, " ", cn)
            # elif len(st) > 5 and score_jaro <= 3:
            #     writer.writerow({"Geo Title": st, "Cornu Title": cn, "Method": "levenstein <= 2", "Score": score_jaro,
            #                      "Status": "NA"})





# score = c.get_raw_score(["test"],["testi"])
# score2 = jac.get_raw_score(["test","aaa"],["testi","aaa"])
# score3 = jaro.get_raw_score("test","testii")
# print(score3)