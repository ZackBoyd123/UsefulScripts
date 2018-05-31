#!/usr/bin/python3
import sys
import csv
import copy
import argparse
import math
from scipy import stats
parser = argparse.ArgumentParser(description="I need -1, -2 and --sample")
parser.add_argument("--first",help="First input file",required=True)
parser.add_argument("--second",help= "Second input file", required=True)
parser.add_argument("--sample",help="Unique sample name i.e Tag1",required=True)
args = parser.parse_args()
file1 = args.first
file2 = args.second
sample = args.sample
sys.stdout = open(sample+"_output.txt", "w")
def read_file(filename):
    position_list = []
    allele_list = []
    with open(filename) as file:
        data = csv.reader(file, delimiter="\t")
        next(data, None)
        for line in data:
            position_list.append(line[1])
            allele_list.append(line[7])
        file.close()

    position_list = [i.replace(" ","")for i in position_list]
    updated_allele_list = []
    for i in allele_list:
        i = i.split(";")[1].strip("AF=")
        updated_allele_list.append(i)
    updated_allele_list = [float(i) for i in updated_allele_list]
    #updated_allele_list = [math.log10(i) for i in updated_allele_list]
    #updated_allele_list = [i ** 2 for i in updated_allele_list]
    return position_list, updated_allele_list


print("Location"+","+"Allele_Frequency_Sample_1"+","+"Allele_Frequency_Sample_2"+","+"Description"+","+"Sample")
location_file_one = read_file(file1)[0]
af_file_one = read_file(file1)[1]
location_file_two = read_file(file2)[0]
af_file_two = read_file(file2)[1]


dictionary_file1 = dict(zip(location_file_one,af_file_one))
dictionary_file2 = dict(zip(location_file_two,af_file_two))
unique_dict1 = copy.deepcopy(dictionary_file1)
unique_dict2 = copy.deepcopy(dictionary_file2)
array_1 = []
array_2 = []
shared_array = []
for i in dictionary_file1:
    if i in dictionary_file2:
        print(str(i)+","+str(dictionary_file1[i])+","+str(dictionary_file2[i])+","+"Shared"+","+str(sample))
        array_1.append(dictionary_file1[i])
        array_2.append(dictionary_file2[i])
        shared_array.append(dictionary_file2[i])
        del unique_dict1[i]
        del unique_dict2[i]

for i in unique_dict1:
    print(str(i)+","+str(dictionary_file1[i])+","+"0"+","+"file_1"+","+str(sample))
    array_1.append(dictionary_file1[i])
    array_2.append(float(0))
for i in unique_dict2:
    print(str(i)+","+"0"+","+str(dictionary_file2[i])+","+"file_2"+","+str(sample))
    array_1.append(float(0))
    array_2.append(dictionary_file2[i])


#####
sys.stdout.close()
sys.stdout = sys.__stdout__
sys.stdout = open(str(sample)+"_stats.txt","w")
#af_ranked1 = stats.rankdata(array_1)
#af_ranked2 = stats.rankdata(array_2)
# data_frame = pandas.DataFrame({"Allele_1": array_1, "Allele_2": array_2})
# data_frame.sort_values(by=["Allele_1"])
# data_frame["Rank"] = data_frame["Allele_1"].rank(ascending=True)
# data_frame.sort_values(by=["Allele_2"])
# data_frame["Rank_Allele_2"] = data_frame["Allele_2"].rank(ascending=True)
# print(data_frame.corr(method="spearman"))

# Tot num of snps, file 1
print("Legend"+","+"File_One_Unique"+","+str(len(unique_dict1))+","+"Legend"+","+str(sample))
# Tot num of snps, file 2
print("Legend"+","+"File_Two_Unique"+","+str(len(unique_dict2))+","+"Legend"+","+str(sample))
# shared SNPs
print("Legend"+","+"Shared_SNPs"+str(len(shared_array))+","+"Legend"+","+str(sample))

#Get sum of squared score
sum_of_squares = []
for a, b in zip(array_1, array_2):
    sum_of_squares.append(math.sqrt((a-b)**2))
print("Legend"+","+"Sum_of_Squares"+","+str(sum(sum_of_squares))+","+"Legend"+","+str(sample))

# Spearman stats
x = (stats.spearmanr(array_1,array_2))
print("Legend"+","+"Spearman_Correlation"+","+str(x[0])+","+"Legend"+","+str(sample))
print("Legend"+","+"Spearman_P-value"+","+str(x[1])+","+"Legend"+","+str(sample))
#print(x)
#####

