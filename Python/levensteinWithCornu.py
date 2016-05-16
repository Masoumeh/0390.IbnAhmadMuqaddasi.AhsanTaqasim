import io
import csv, json

def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings."""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for x in range(first_length)]
    for i in range(first_length):
       distance_matrix[i][0] = i
    for j in range(second_length):
       distance_matrix[0][j]=j
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]
sttls =[]
with open('Shamela_0023696_Triples_H', 'r') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='|')
  with open ('cornu.csv') as cornu:
    data = csv.reader(cornu, delimiter=',', quotechar='|')
    next(data, None)
    for row in reader:
      sttl = row[-1][4:].strip()
      cnt = 0
      for d in data:
        print("d2 ",d[2])
        if levenshtein_distance(d[2],sttl) <= 2:
           print("sttl ", sttl)
#if d["arTitle"] == sttl:
#             cnt = cnt+1
#             sttls.append(sttl)            
#print (sttls)
