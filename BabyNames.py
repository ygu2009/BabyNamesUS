"""
This code is to answer the following questions on the data set of Baby Names from 1910 to 2014

1.  What is the most popular name of all time? (Of either gender.)
2.  What is the most gender ambiguous name in 2013? 1945?
3.  Of the names represented in the data, find the name that has had the largest
    percentage increase in popularity since 1980. Largest decrease?
4.  Can you identify names that may have had an even larger increase or decrease
    in popularity?


The data can be downloaded in zip format from:
http://www.ssa.gov/oact/babynames/state/namesbystate.zip

Implemented in Python 2.7.11 by Yingying Gu.
Date: 04/02/2016
"""
import numpy as np
import math
import os



def load_data(path):
    """
    The function is to read the data from all files in a given path directory

    :param path: a given data file directory './namesbystate/'
    :return: lists of data in all files
    """
    contents = [] # list for collecting all the data together
    for file in os.listdir(path):  # get each file from a directory
        print path+file
        with open(path+file,'r') as f:  # read each file
            for line in f:
                t = line[:-1].split(',') # split each value between ',' and remove '\n' in the end of each line
                tmp = []
                for item in t:
                    try:
                        item = int(item)
                        tmp.append(item)  # string number to integer
                    except:
                        tmp.append(item) # keep the string
                contents.append(tmp)
    return contents


def merging_by_name(data, years):
    """
    The function is to combine/merge all the same names all over US states in given years

    :param data: raw data from load_data
    :param years: for example, range(2013, 2014) or range(1910, 2015)
    :return: Each row is unique name, column is counts of F/M, F, M
    """
    name_counts = []
    current_name = None
    current_count = 0
    F_count = 0
    M_count = 0
    for n in range(data.shape[0]):
        if data[n, 2] in years:  # choose the years that we want to search into
            name, count, sex = data[n,3], data[n,4], data[n,1]
            if current_name == name:  # merge the same name from different states
                if sex == 'F':  # compute the F counts
                    F_count += count
                if sex == 'M':  # compute the F counts
                    M_count += count
            else:
                if current_name: # merging the same name
                    if F_count == 0 or M_count == 0:
                        entropy = 0.0
                    else:
                        F_ratio = (F_count+0.0)/(F_count+M_count)
                        M_ratio = (M_count+0.0)/(F_count+M_count)
                        entropy = - F_ratio * math.log(F_ratio) - M_ratio * math.log(M_ratio)  # F and M name difference by entropy=-xlog(x)
                    name_counts.append([current_name, F_count, M_count, entropy])
                current_name = name
                if sex == 'F':
                    F_count = count
                    M_count = 0
                if sex == 'M':
                    F_count = 0
                    M_count = count
    if current_name == name:  # adding the last name
        if F_count == 0 or M_count == 0:
            entropy = 0
        else:
            F_ratio = (F_count+0.0)/(F_count+M_count)
            M_ratio = (M_count+0.0)/(F_count+M_count)
            entropy = - F_ratio * math.log(F_ratio) - M_ratio * math.log(M_ratio) # F and M name difference by entropy
        name_counts.append([current_name, F_count, M_count,  entropy])
    name_counts = np.array(name_counts,dtype=object)
    return name_counts


def build_name_counts_year_matrix(data):
    """
    The function is to build a (name, counts@year) matrix from year 1910 to 2014 in US.
    Each row is unique name, each column is the counts in year

    :param data: raw data from load_data
    :return: (name, total_counts, counts@year) matrix :
    """
    name_counts_in_year = []
    current_name = None
    current_count = 0
    year_count = np.zeros([2014-1910+1])
    for n in range(data.shape[0]):
        name, count, year = data[n,3], data[n,4], data[n,2]
        if current_name == name:
            current_count += count
            year_count[year-1910] += count # counts@year from 1910 to 2014
        else:
            if current_name:
                tmp=[]
                tmp.extend([current_name, current_count])
                tmp.extend(year_count)
                name_counts_in_year.append(tmp)
            current_name = name
            year_count = np.zeros([2014-1910+1])
            year_count[year-1910] += count
            current_count = count
    if current_name == name:  # adding the last name
        tmp=[]
        tmp.extend([current_name, current_count])
        tmp.extend(year_count)
        name_counts_in_year.append(tmp)
    name_counts_in_year = np.array(name_counts_in_year,dtype=object)
    return name_counts_in_year


if __name__ == '__main__':

    # load/read the data from files
    path = './namesbystate/'
    data = load_data(path)

    # change the list to array (easy to access and retrieve)
    data=np.array(data, dtype=object)

    # sort all by name
    data = data[data[:,3].argsort()] # sort by names alphabet order

    # 1. What is the most popular name of all the time (starting from 1910)? (Of either gender)
    # merge/count by name according to the years
    # The columns are: name, total counts, F counts, M counts, name entropy of F ratio and M ratio
    years = range(1910,2015)
    names_freqs = merging_by_name(data, years)
    # print the top 5 popular names from 1910 to 2014
    # top 5 M/F names
    total_counts = names_freqs[:,1] + names_freqs[:,2]
    sorted_names_by_counts = names_freqs[(-total_counts).argsort()] # sort by name_counts = most popular names
    print "Top M/F name rank:"
    for i in range(5):
        print "Rank %d: %s, F/M: %d" % (i+1, sorted_names_by_counts[i,0], sorted_names_by_counts[i,1]+sorted_names_by_counts[i,2])
    # top 5 F names
    sorted_names_by_counts = names_freqs[(-names_freqs[:,1]).argsort()] # sort by name_counts = most popular names
    print "Top F name rank:"
    for i in range(5):
        print "Rank %d: %s, F: %d, M: %d" % (i+1, sorted_names_by_counts[i,0], sorted_names_by_counts[i,1], sorted_names_by_counts[i,2])
    # top 5 M names
    sorted_names_by_counts = names_freqs[(-names_freqs[:,2]).argsort()] # sort by name_counts = most popular names
    print "Top M name rank:"
    for i in range(5):
        print "Rank %d: %s, F: %d, M: %d" % (i+1, sorted_names_by_counts[i,0], sorted_names_by_counts[i,1], sorted_names_by_counts[i,2])

    # 2. What is the most gender ambiguous name in 2013? 1945?
    years = range(2013,2014) #(2013,2014) or (1945,1946)
    names_freqs = merging_by_name(data, years)
    sort_by_gender_ambiguous_name = names_freqs[(-names_freqs[:,3]).argsort()]  #sort by entropy between F and M = gender ambiguous name
    # print most gender ambiguous name to at least 1000 babies
    # The columns are: name, total counts, F counts, M counts, name entropy of F ratio and M ratio
    sorted_by_gender_ambiguous = sort_by_gender_ambiguous_name[sort_by_gender_ambiguous_name[:,1] > 1000]
    print "Most gender ambigous name in year %d:" % years[0]
    for i in range(5):
        print "Rank %d: %s, F: %d, M: %d, Entropy: %0.5f" % (i+1, sorted_by_gender_ambiguous[i,0],sorted_by_gender_ambiguous[i,1],
                                                             sorted_by_gender_ambiguous[i,2], sorted_by_gender_ambiguous[i,3])

    # 3. find the name that has had the largest percentage increase in popularity since 1980. Largest decrease
    # merge by name and recording the name counts according to year from 1910 to 2014
    names_freqs_years = build_name_counts_year_matrix(data)
    count_by_year = names_freqs_years[:,2:]
    M, N = count_by_year.shape # M rows, N cols

    counts_in_year_1980 = count_by_year[:,1980-1910]  # extract the columns in 1980 from data
    counts_in_year_2014 = count_by_year[:,2014-1910]  # extract the columns in 2014 from data

    # Largest percentage increase since 1980
    increase = np.zeros(M)
    for i in range(M):
        if counts_in_year_1980[i] > 0: # for names which exists in 1980
            increase[i] = (counts_in_year_2014[i] - counts_in_year_1980[i]) / (counts_in_year_1980[i]+0.0) * 100.0
        else:
            increase[i] = 0 # for name is not appeared in 1980, and not included into calculation
    sorted_names_by_increases = names_freqs_years[(-increase).argsort(),0] # sort the matrix by using the increase percentage
    print "Largest percentage increase since 1980: "
    for i in range(5):
        print "Rank %d: %s, Increases: %d%%" % (i+1, sorted_names_by_increases[i], increase[(-increase).argsort()][i])

    # Largest percentage decrease since 1980
    decrease = np.zeros(M)
    for i in range(M):
        if counts_in_year_2014[i] > 0: # for names which exists in 2014
            decrease[i] = (counts_in_year_1980[i] - counts_in_year_2014[i]) / (counts_in_year_2014[i]+0.0) * 100.0
        else:
            decrease[i] = 0 # for name is not appeared in 2014, and not included into calculation
    sorted_names_by_decreases = names_freqs_years[(-decrease).argsort(),0]  # sort the matrix by using the decrease percentage
    print "Largest percentage decrease since 1980: "
    for i in range(5):
        print "Rank %d: %s, Increases: %d%%" % (i+1, sorted_names_by_decreases[i], decrease[(-decrease).argsort()][i])

    # 4. identify names that may have had an even larger increase or decrease in popularity
    # Yes, the names may not exists in 1980 but exist in 2014
    # Largest percentage increase since 1980
    increase = np.zeros(M)
    for i in range(M):
        if counts_in_year_1980[i] == 0: # for names which exists in 2014 but not in 1980 and add 1.0 in 1980 to avoid divide by 0
            increase[i] = (counts_in_year_2014[i] - counts_in_year_1980[i]) / (counts_in_year_1980[i]+1.0) * 100.0
        else:
            increase[i] = (counts_in_year_2014[i] - counts_in_year_1980[i]) / (counts_in_year_1980[i]) * 100.0
    sorted_names_by_increases = names_freqs_years[(-increase).argsort(),0] # sort the matrix by using the increase percentage
    print "Largest percentage increase since 1980: "
    for i in range(5):
        print "Rank %d: %s, Increases: %d%%" % (i+1, sorted_names_by_increases[i], increase[(-increase).argsort()][i])

    # Largest percentage decrease since 1980
    decrease = np.zeros(M)
    for i in range(M):
        if counts_in_year_2014[i] == 0: # for names which exists in 1980 but not in 2014 and add 1.0 in 2014 to avoid divide by 0
            decrease[i] = (counts_in_year_1980[i] - counts_in_year_2014[i]) / (counts_in_year_2014[i]+1.0) * 100.0
        else:
            decrease[i] = (counts_in_year_1980[i] - counts_in_year_2014[i]) / (counts_in_year_2014[i]) * 100.0
    sorted_names_by_decreases = names_freqs_years[(-decrease).argsort(),0]  # sort the matrix by using the decrease percentage
    print "Largest percentage decrease since 1980: "
    for i in range(5):
        print "Rank %d: %s, Increases: %d%%" % (i+1, sorted_names_by_decreases[i], decrease[(-decrease).argsort()][i])





