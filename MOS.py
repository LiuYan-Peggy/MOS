# -*- coding: utf-8 -*-

"""
Change the input network name or path in lines 261-263
"""
import networkx as nx
import numpy as np
from scipy.stats import *
from sir import *
np.set_printoptions(threshold=np.inf)
import rpy2.robjects as robjects
import pandas as pd
import math



def quantile_exc(data_sort, n):
    if n < 1 or n > 3:
        return "False"
    position = (len(data_sort) + 1)*n/4
    # math.modf(100.12) :  (0.12000000000000455, 100.0)
    pos_integer = int(math.modf(position)[1])
    quartile = data_sort[pos_integer - 1]
    return quartile

def distance_mat(G):
    dis = np.zeros((N, N), dtype=object)
    for i in range(N):
        source = index_node[i]  # source node name
        dis[i][i] = (0, G.degree(source))
        for j in range(i+1, N):
            target = index_node[j]  # target node name
            if nx.has_path(G, source, target):
                distance = nx.shortest_path_length(G, source, target)
                dis[i][j] = (distance, G.degree(target))
                dis[j][i] = (distance, G.degree(source))
            else:
                dis[i][j] = (N, G.degree(target))
                dis[j][i] = (N, G.degree(source))
    return dis

def FI(dis_mat, rank_num):
    c = {}
    for i in range(N):
        array = dis_mat[i, :]
        array_new = np.delete(array, i)
        a_sort = sorted(array_new, key=lambda x: (x[0], -x[1]))
        tuple = a_sort[rank_num - 1]
        c[i] = tuple
    c_sort = sorted(c.items(), key=lambda x: (x[1][0], -x[1][1]))
    r = 0
    pos = 0
    score = {}
    pre = 0
    for x, y in c_sort:
        if pos == 0:
            pre = y
            r += 1
            score[x] = r
            pos += 1
        else:
            if y == pre:
                score[x] = r
                r += 0
                pos += 1
            else:
                pre = y
                r = pos + 1
                score[x] = r
                pos += 1
    c_list = [0] * N
    c_final = {}
    for i in range(N):
        final_score = N + 1 - score[i]
        c_list[i] = final_score
        c_final[i] = final_score
    c_set = set(c_list)
    num_disdinct_count = len(c_set)
    return c_list, num_disdinct_count

def count_quantile(dis_mat, quantile_n):
    c = {}
    for i in range(N):
        array = dis_mat[i, :]
        array_new = np.delete(array, i)

        array_new = list(array_new)
        array_new_sort = sorted(array_new, key=lambda x: (x[0], -x[1]))
        array_new = []
        for x, y in array_new_sort:
            if x == 1:
                array_new.append((x, y))
            else:
                break

        quantile_value = quantile_exc(array_new, quantile_n)
        array_new.append(quantile_value)
        a_sort = sorted(array_new, key=lambda x: (x[0], -x[1]))
        count = a_sort.index(quantile_value)
        for j in range(count+1, len(a_sort)):
            if a_sort[j] == quantile_value:
                count += 1
            else:
                break
        c[i] = count
    c_list = [0] * N
    for i in range(N):
        c_list[i] = c[i]
    c_set = set(c_list)
    num_disdinct_count = len(c_set)
    return c_list, num_disdinct_count

def count_mean(dis_mat, level):
    c = {}
    for i in range(N):
        array = dis_mat[i, :]
        array_new = np.delete(array, i)
        array_new = list(array_new)
        num = 0
        sum_1 = 0
        for x,y in array_new:
            if x == level:
              sum_1 += y
              num += 1
        new_tuple = (1, sum_1 / num)
        array_new.append(new_tuple)
        a_sort = sorted(array_new, key=lambda x: (x[0], -x[1]))
        count = a_sort.index(new_tuple)
        for j in range(count+1, len(a_sort)):
            if a_sort[j] == new_tuple:
                count += 1
            else:
                break
        c[i] = count
    c_list = [0] * N
    for i in range(N):
        c_list[i] = c[i]
    c_set = set(c_list)
    num_disdinct_count = len(c_set)
    return c_list, num_disdinct_count

def FS(dis_mat, new_tuple):
    c = {}
    for i in range(N):
        array = dis_mat[i, :]
        array_new = np.delete(array, i)
        array_new = list(array_new)
        array_new.append(new_tuple)
        a_sort = sorted(array_new, key=lambda x: (x[0], -x[1]))
        count = a_sort.index(new_tuple)
        for j in range(count+1, len(a_sort)):
            if a_sort[j] == new_tuple:
                count += 1
            else:
                break
        c[i] = count
    c_list = [0] * N
    for i in range(N):
        c_list[i] = c[i]
    c_set = set(c_list)
    num_disdinct_count = len(c_set)
    return c_list, num_disdinct_count


def new_score(c_list):
    c_set = set(c_list)
    c_sort = sorted(c_set, reverse=False)
    c_dict = {}
    c_len = len(c_sort)
    for i in range(len(c_sort)):
        score = c_sort[i]
        c_dict[score] = c_len - i
    num = len(c_set)
    new = []
    for j in range(len(c_list)):
        pre_value = c_list[j]
        new_value = c_dict[pre_value] / num
        new.append(new_value)
    return new


def main(G):
    dis_mat = distance_mat(G)

    print("*************FS****************")
    fix_tuple = [(1, 2), (1, 4), (1, 6), (1, 8), (1, 10)]
    fix_count = 0
    fix_list = []
    for i in range(len(fix_tuple)):
        fix_num = fix_tuple[i]
        c_list, num_disdinct_count = FS(dis_mat, fix_num)
        if num_disdinct_count > fix_count:
            fix_count = num_disdinct_count
            fix_list = c_list


    print("*************AS****************")
    quan_list = [1, 2, 3]
    quantile_count = 0
    quantile_list = []
    for i in range(len(quan_list)):
        quantile_num = quan_list[i]
        c_list, num_disdinct_count = count_quantile(dis_mat, quantile_num)
        if num_disdinct_count >= quantile_count:
            quantile_count = num_disdinct_count
            quantile_list = c_list
    # print(quantile_count)
    c_list, num_disdinct_count = count_mean(dis_mat, 1)
    if num_disdinct_count >= quantile_count:
        quantile_list = c_list


    print("*************FI****************")
    rank_num_list = [0.1, 0.2, 0.4, 0.6, 0.8]
    rank_count = 0
    rank_list = []
    for i in range(len(rank_num_list)):
        rank_num = rank_num_list[i]
        c_list, num_disdinct_count = FI(dis_mat, int(rank_num * (N - 1)))
        if num_disdinct_count >= rank_count:
            rank_count = num_disdinct_count
            rank_list = c_list

    # robjects.FloatVector returns recognizable type of R language
    c_1_new = robjects.FloatVector(new_score(quantile_list))
    c_5_new = robjects.FloatVector(new_score(fix_list))
    c_50_new = robjects.FloatVector(new_score(rank_list))
    robjects.r.source('RRA.r')
    df = robjects.r.rbind(c_1_new, c_5_new, c_50_new)
    robjects.r.rra(df, N)
    result = pd.read_csv("rra.csv")

    final_score = {}
    for i in range(N):
        node_name = index_node[result.iloc[i, 0] - 1]
        value = result.iloc[i, 2]
        final_score[node_name] = value
    final = {}
    for node in G.nodes():
        final[node] = final_score[node]

    print("\n")
    print("===================MOS-index result====================")
    print("MOS-index: ", final)
    print(sorted(final.items(), key=lambda k:k[1], reverse=False))

    print('number of nodes：%d' % (N))
    print('number of edges：%d' % (M))
    print("Network name: %s" % (name))

if __name__ == '__main__':
    network = ["karate", "USpowerGrid", "ia-reality", "jazz", "dolphins", "email-univ", "ns",
               "USair_unweighted", "Political blogs", "Router", "HI", "football", "911", "abn", "dbn", "mbn", "Bahia",
               "baydry", "Bluthgen", "Carpinteria", "ca-CSphd", "ca-GrQc", "celegans_metabolic", "celegans_Phenotypes",
               "crystal", "Estero", "Everglades", "Florida", "Galesburg", "Galesburg2", "glossGT", "grass_web", "geom",
               "gramdry", "Korea1", "Korea2", "Maspalomas", "mexican_power", "Michigan", "Mondego", "movies",
               "personal", "russiantrade", "SciMet", "sep_fall98", "SmaGri", "SmallW", "StMarks", "stormofswords",
               "Sylt", "world_trade", "yeast_ito", "Ythan"]

    name = 'karate'
    net_path = r"C:/data" + "/" + name + ".txt"
    G = nx.read_edgelist(net_path, delimiter='\t', nodetype=str)

    global M, N, node_index, index_node
    N = G.number_of_nodes()
    M = G.number_of_edges()
    node_index = {}
    index_node = {}
    index = 0
    for node in G.nodes():
        index_node[index] = node
        node_index[node] = index
        index += 1

    main(G)

