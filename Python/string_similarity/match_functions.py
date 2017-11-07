from aratext import normalization as norm
import global_var as gv
from fuzzywuzzy import fuzz
import jellyfish as jf
import jellyfish._jellyfish as py_jellyfish
import py_stringmatching as ps



def find_match(match_funct, cornu_places, sttl_reg, cornu_matched_list):
  """
  
  :param cornu_places: cornu places
  :param sttl_reg: the string containing the toponym in question together with the province it belongs (topo-province)
  :return
  """
  # print(sttl_reg)
  sttl_name = sttl_reg.split('/')[0]
  reg = sttl_reg.split('/')[1]
  match_list = []
  # print("m reg:", reg)
  for f in cornu_places["features"]:
      if f["properties"]["cornuData"]["cornu_URI"] not in cornu_matched_list:
          cornu_title = f["properties"]["cornuData"]["toponym_arabic"]
          cornu_title_other = f["properties"]["cornuData"]["toponym_arabic_other"].split("،")
          cornu_reg = f["properties"]["cornuData"]["region_spelled"] # region_code should be here normally
          # print("c reg: ",cornu_reg)
          # if sc.qgram(sttl_name, cornu_title, q=4, common_divisor = 'average', min_threshold = 0.95,
          # padded=True) and cornu_reg in gv.reg_dict[reg]:
          #     match_list.append(get_match(sttl_reg, f))
          # else:
          #     for n in cornu_title_other:
          #         n = n.strip()
          #         if sc.qgram(sttl_name, n, q=2, common_divisor='average', min_threshold=0.8,
          #                     padded=True) and cornu_reg in gv.reg_dict[reg]:
          #             match_list.append(get_match(sttl_reg, f))
          if match_funct(sttl_name, reg, cornu_title, cornu_reg):
              match_list.append(get_match(sttl_reg, f))
          else:
              for n in cornu_title_other:
                  n = n.strip()
                  if match_funct(sttl_name, reg, n, cornu_reg):
                      match_list.append(get_match(sttl_reg, f))
  # print("mathclist: ",match_list)
  return match_list if len(match_list) != 0 else None

def find_match_node(match_funct, cornu_places, node, cornu_matched_list):
  """
  
  :param cornu_places: cornu places
  :param node: the string containing the toponym in question 
  :return
  """

  match_list = []
  for f in cornu_places["features"]:
      if f["properties"]["cornuData"]["cornu_URI"] not in cornu_matched_list:
          cornu_title = f["properties"]["cornuData"]["toponym_arabic"]
          cornu_title_other = f["properties"]["cornuData"]["toponym_arabic_other"].split("،")
          cornu_reg = f["properties"]["cornuData"]["region_code"]
          # if sc.qgram(sttl_name, cornu_title, q=4, common_divisor = 'average', min_threshold = 0.95,
          # padded=True) and cornu_reg in gv.reg_dict[reg]:
          #     match_list.append(get_match(sttl_reg, f))
          # else:
          #     for n in cornu_title_other:
          #         n = n.strip()
          #         if sc.qgram(sttl_name, n, q=2, common_divisor='average', min_threshold=0.8,
          #                     padded=True) and cornu_reg in gv.reg_dict[reg]:
          #             match_list.append(get_match(sttl_reg, f))
          if match_funct(node, cornu_title):
              match_list.append((node, f))
          else:
              for n in cornu_title_other:
                  n = n.strip()
                  if match_funct(node, n):
                      match_list.append((node, f))
  # print("mathclist: ",match_list)
  return match_list if len(match_list) != 0 else None


def get_match(sttl_reg, cornu_feature):
    match_dict = {}
    match_dict[sttl_reg] = {}
    match_dict[sttl_reg]["Geo Prov"] = sttl_reg.split("/")[1]
    match_dict[sttl_reg]["Cornu feature"] = cornu_feature
    return match_dict


def apply_match(funct, args):
    funct(*args)


def fuzzy_match(topo_name, topo_reg, cornu_title, cornu_reg):
    if fuzz.ratio(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title)) >= 90 and \
                    cornu_reg in gv.reg_dict[topo_reg]:
        return True


def fuzzy_partial_match(topo_name, topo_reg, cornu_title, cornu_reg):
    if fuzz.partial_ratio(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title)) >= 90 and \
                    cornu_reg in gv.reg_dict[topo_reg]:
        return True


def dam_levenstein_match(topo_name, topo_reg, cornu_title, cornu_reg):
    lev_dist = py_jellyfish.damerau_levenshtein_distance(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title))
    if lev_dist <= 2:
        # and cornu_reg in gv.reg_dict[topo_reg]:
        return True
    else:
        return False


def levenstein_match(topo_name, topo_reg, cornu_title, cornu_reg):
    lev_dist = jf.levenshtein_distance(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title))
    if lev_dist <= 2:
        # and cornu_reg in gv.reg_dict[topo_reg]:
        print(lev_dist)
        return True
    else:
        return False


def jaro_match(topo_name, topo_reg, cornu_title, cornu_reg):
    jaro_dist = jf.jaro_distance(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title))
    if jaro_dist >= 0.85\
        and (cornu_reg in topo_reg or cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
                    # cornu_reg in gv.reg_dict[topo_reg]:
        # print(jaro_dist, " ", topo_name, " ", cornu_title)
        return True
    else:
        return False

def jaro_noReg_match(topo_name, topo_reg, cornu_title, cornu_reg):
    jaro_dist = jf.jaro_distance(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title))
    if jaro_dist >= 0.85:
        # print(jaro_dist, " ", topo_name, " ", cornu_title)
        return True
    else:
        return False

def jaroW_match(topo_name, topo_reg, cornu_title, cornu_reg):
    jaro_dist = jf.jaro_winkler(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title))
    if jaro_dist >= 0.90 and jaro_dist < 1 and \
            (cornu_reg in topo_reg or cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False

def jaroW_noReg_match(topo_name, topo_reg, cornu_title, cornu_reg):
    jaro_dist = jf.jaro_winkler(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title))
    if jaro_dist >= 0.85 and jaro_dist < 1: # and cornu_reg in gv.reg_dict[topo_reg]:
        return True
    else:
        return False

def hamming_match(topo_name, topo_reg, cornu_title, cornu_reg):
    hamming_dist = jf.hamming_distance(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title))
    if hamming_dist <= 2 \
            and (cornu_reg in topo_reg or
                         cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False



def exact_match(topo_name, topo_reg, cornu_title, cornu_reg):
    if (norm.normalize_alphabet(topo_name) == norm.normalize_alphabet(cornu_title) or \
                    topo_name == cornu_title) and \
            (cornu_reg in topo_reg or cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
                    # any(cornu_reg in i for i in [gv.reg_dict[topo_reg], topo_reg]):
        return True
    else:
        return False


def exact_noReg_match(topo_name, topo_reg, cornu_title, cornu_reg):
    if (norm.normalize_alphabet(topo_name) == norm.normalize_alphabet(cornu_title) or \
                    topo_name == cornu_title):
        return True
    else:
        return False


def exact_node_match(node, cornu_title):
    if (norm.normalize_alphabet(node) == norm.normalize_alphabet(cornu_title) or \
                    node == cornu_title) :
        return True
    else:
        return False


def monge_elkan_match(topo_name, topo_reg, cornu_title, cornu_reg):
    ws_tok = ps.WhitespaceTokenizer(return_set=True)
    topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    me = ps.MongeElkan()
    monge_elkan = me.get_raw_score(topo_name_list, cornu_list)
    if monge_elkan >= 0.9:
        # and (cornu_reg in topo_reg or cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False


def jaccard_match(topo_name, topo_reg, cornu_title, cornu_reg):
    ws_tok = ps.WhitespaceTokenizer(return_set=True)
    topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    jac = ps.Jaccard()
    jaccard = jac.get_sim_score(topo_name_list, cornu_list)
    # if jaccard> 0.0:
    #     print(jaccard)
    if jaccard >= 0.5:
            # and (cornu_reg in topo_reg or cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False


def cosine_match(topo_name, topo_reg, cornu_title, cornu_reg):
    ws_tok = ps.WhitespaceTokenizer(return_set=True)
    topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    cos = ps.Cosine()
    cosine = cos.get_raw_score(topo_name_list, cornu_list)
    # if jaccard> 0.0:
    #     print(jaccard)
    if  cosine>= 0.65\
            and (cornu_reg in topo_reg or
                         cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False


def overlap_coefficient_match(topo_name, topo_reg, cornu_title, cornu_reg):
    ws_tok = ps.WhitespaceTokenizer(return_set=True)
    topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    oc = ps.OverlapCoefficient()
    over_co = oc.get_sim_score(topo_name_list, cornu_list)
    # if jaccard> 0.0:
    #     print(jaccard)
    if  over_co >= 0.5 and over_co < 1:
        # and (cornu_reg in topo_reg or
        #      cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False


def affine_match(topo_name, topo_reg, cornu_title, cornu_reg):
    # ws_tok = ps.WhitespaceTokenizer(return_set=True)
    # topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    # cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    aff = ps.Affine(gap_start=2, gap_continuation=0.5, sim_func=lambda s1, s2: (int(1 if s1 == s2 else 0)))
    affine = aff.get_raw_score(topo_name, cornu_title)
    if affine <= 3:
        # and \
        # (cornu_reg in topo_reg or
        #              cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False


def dice_match(topo_name, topo_reg, cornu_title, cornu_reg):
    ws_tok = ps.WhitespaceTokenizer(return_set=True)
    topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    di = ps.Dice()
    dice = di.get_sim_score(topo_name_list, cornu_list)
    if dice >= 0.5:
        # and (cornu_reg in topo_reg or
        #      cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False

def needleman_match(topo_name, topo_reg, cornu_title, cornu_reg):
    # ws_tok = ps.WhitespaceTokenizer(return_set=True)
    # topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    # cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    nw = ps.NeedlemanWunsch(gap_cost=1.0, sim_func=lambda s1, s2 : (2.0 if s1 == s2 else -1.0))
    needleman = nw.get_raw_score(topo_name, cornu_title)
    if needleman >= 0.98 :
        # and (cornu_reg in topo_reg or
        #              cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False


def smith_match(topo_name, topo_reg, cornu_title, cornu_reg):
    # ws_tok = ps.WhitespaceTokenizer(return_set=True)
    # topo_name_list = ws_tok.tokenize(norm.normalize_alphabet(topo_name))
    # cornu_list = ws_tok.tokenize(norm.normalize_alphabet(cornu_title))
    sw = ps.SmithWaterman(gap_cost=2, sim_func=lambda s1, s2: (2 if s1 == s2 else -1))
    smith = sw.get_raw_score(topo_name, cornu_title)
    if smith == 2:
            # and (cornu_reg in topo_reg or
            #              cornu_reg in (gv.reg_dict[topo_reg] if topo_reg in gv.reg_dict else "null")):
        return True
    else:
        return False


