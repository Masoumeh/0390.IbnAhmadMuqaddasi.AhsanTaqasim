import get_sttl_reg as gsr
import numpy as np

def write_sample_file(data_file, write_file):
    muq_sttls = list(gsr.get_sttl(data_file))
    sample_index = np.random.choice(1200, 100)
    with open(write_file, 'w', encoding="utf8") as samples_file:
        for i in sample_index:
            sttl = muq_sttls[i]
            print(sttl)
            samples_file.write(sttl + "\n")




write_sample_file("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all",
                  "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/sample_data")