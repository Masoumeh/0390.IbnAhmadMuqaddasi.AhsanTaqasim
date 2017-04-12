"""
Create Matrix for cornu data in two levels (regions and settlements)
"""
import csv, json
import io
import scipy.sparse as sps
import numpy as np
import pandas as pd
import pprint 


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def creatMatrix (cornuFile, geoFile):
  with open(cornuFile, "r", encoding="utf8") as cornu:
      cornu = json.load(cornu)
      cornu_regs = [d for d in cornu]
      cornu_topos = [d for d in cornu[cornu_regs[0]]]

      with open(geoFile, "r", encoding="utf8") as geo:
          geo = json.load(geo)
          geo_regs = [d for d in geo]
          #print(geo_regs[0])
          geo_topos = [d for d in geo[geo_regs[0]]]

          all_regs = list(set().union(cornu_regs, geo_regs))
          all_topos = list(set().union(cornu_topos, geo_topos))
          #print(json.dumps(all_topos, indent=4, sort_keys=True,ensure_ascii=False,))
          all_dict = cornu.copy()
          all_dict.update(geo)
          #geo_matrix = [[(t for t in all_topos, [0 for t in range(len(all_topos))]) for r in range(len(geo_regs))]]
          #cornu_matrix = [[(t for t in all_topos, [0 for t in range(len(all_topos))]) for r in range(len(cornu_regs))]]
          #print(pd.DataFrame.from_items([[(t for t in all_topos, [0 for t in range(len(all_topos))]) for r in range(len(all_regs))]], columns=all_regs))
          #cornu_matrix = pd.DataFrame(0, index=np.arange(len(all_topos)), columns=cornu_regs)
           
          geo_matrix = pd.DataFrame.from_dict(geo, dtype = object)
          # replace white spaces with "_" in column names
          geo_matrix.columns =[x.strip().replace(' ', '_') for x in geo_matrix.columns]
          cornu_matrix = pd.DataFrame.from_dict(cornu, dtype = object)
          # replace white spaces with "_" in column names
          cornu_matrix.columns = [x.strip().replace(' ', '_') for x in cornu_matrix.columns]
          cornu_matrix['Jazirat_al-Arab,Yemen'] = cornu_matrix['Jazirat_al-Arab'].values | cornu_matrix['Yemen'].values
          cornu_matrix['Maghrib,Barqa,Andalus'] = cornu_matrix['Maghrib'].values | cornu_matrix['Barqa'].values | cornu_matrix['Andalus'].values
          cornu_matrix['Khurasan,Sijistan,Transoxiana'] = cornu_matrix['Khurasan'].values | cornu_matrix['Sijistan'].values | cornu_matrix['Transoxiana'].values
          #geo_matrix.fillna(0, inplace=True)
          #cornu_matrix.fillna(0, inplace=True)
          cornu_matrix.drop(['Khurasan', 'Transoxiana', 'Sijistan', 'Jazirat_al-Arab', 'Yemen', 'NoRegion', 'Maghrib','Barqa','Andalus', 'Sicile', 'Khazar', 'Mafaza','Badiyat_al-Arab'], axis=1, inplace=True) 
          common_topos = pd.Series(list(set(cornu_matrix.index).intersection(set(geo_matrix.index))))
          uncommon_topos_for_geo = [a for a in all_topos if a not in geo_topos] 
          uncommon_topos_for_cornu = [a for a in all_topos if a not in cornu_topos]  
          print(len(uncommon_topos_for_cornu))
          df_for_geo = pd.DataFrame(0, index=uncommon_topos_for_geo, columns=geo_matrix.columns)
          df_for_cornu = pd.DataFrame(0, index=uncommon_topos_for_cornu, columns=cornu_matrix.columns)                      
          cornu_matrix = cornu_matrix.append(df_for_cornu, ignore_index=False)
          geo_matrix = geo_matrix.append(df_for_geo, ignore_index=False)
          cornu_matrix.sort_index(inplace=True)
          geo_matrix.sort_index(inplace=True)
          geo_matrix = geo_matrix[sorted(geo_matrix.columns)]
          cornu_matrix = cornu_matrix[sorted(cornu_matrix.columns)]
          geo_matrix.to_csv('geo.csv', index=True)
          cornu_matrix.to_csv('cornu.csv', index=True)
          all_topos_len = len(all_topos)
          cnts = {}

          #print(pd.merge(geo_matrix, cornu_matrix, on=['Iraq'], how='inner')['Iraq'])
          #print(pd.merge(cornu_matrix, geo_matrix, on='Faris',how='left', indicator=True)['_merge'] == 'both')
          commons = []
          with open('../Data/matrixDiff_cornu_geo.csv', 'w') as outfile:
            writer = csv.writer(outfile, delimiter='\t')
            writer.writerow(["region", "Muqaddasi_toponyms", "Cornu_toponyms", "Common_toponyms"])
            for col in geo_matrix:
              tmp1 = geo_matrix.loc[geo_matrix[col] == 1][col]
              tmp2 = cornu_matrix.loc[cornu_matrix[col] == 1][col]
              common_topos = list(set(tmp1.index).intersection(tmp2.index))
              common_len = len(common_topos)
              geo_len = tmp1.size
              cornu_len = tmp2.size
              writer.writerow([col, geo_len, cornu_len, common_len])
                  
  
      #json.dump(commons, outfile, indent=4, sort_keys=True,ensure_ascii=False)


  
creatMatrix ("../Data/matrix_cornu.json", "../Data/matrix_Muq_cornuMatches.json")

          

       
