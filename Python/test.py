import csv


def test (csvFile):
  with open(csvFile, "r", encoding="utf8") as f1:
        f1 = csv.reader(f1, delimiter='\t')
        for r in f1:
          print(r[0].split('\t'))


test ("../Data/matrixDiff_cornu_geo.json")
