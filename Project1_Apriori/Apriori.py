'''
# Programming Assignment 1

* Goal : To find association rules using Apriori algorithm
    - Step1 : find frequent itemsets using Apriori
    - Step2 : for each frequent itemset, find association rules
    
* input.txt
    - Each line : transaction
    - item_id = numerical value
    - no duplication of items in each transaction

* output.txt
    - {item_set} -> {associative_item_set}
    - Use braces ({}) to represent item sets
    - Support : probability that a transaction contains {item_set} U {associative_item_set}
    - Confidence : conditional probability that a transaction having {item_set} also contains {associative_item_set}
    - The value of support and confiddence should be rounded to two decimal places
    
* Execution
 : python 2021088304_박현준_hw1.py 10 input.txt output.txt
'''
import sys 
from itertools import combinations

db_size = 0
transactions = []
min_sup = int(sys.argv[1])
min_sup_freq = 0
frequent_pattern = []
total_itemset = set()

# input file을 읽어서 transaction을 저장하는 함수
def scanDB():
    global db_size, transactions, min_sup_freq, total_itemset
    item_list = []
    
    input_file = open(sys.argv[2], 'r')
    
    while True:
        line = input_file.readline()
         
        if not line:
            break
        
        trx = list(map(int,line.split())) 
        transactions.append(trx)
        for item in trx:
            item_list.append(int(item))

    db_size = len(transactions) # transaction의 개수
    total_itemset = set(item_list) # item의 집합
    min_sup_freq = db_size * (min_sup / 100) # min_sup의 개수
    transactions = list_to_set(transactions) # transaction을 set으로 변환
    
    input_file.close()

# 중복을 제거하기 위해 set으로 변환
def list_to_set(item_list):
    result = []
    for item in item_list:
        result.append(set(item))
    return result

# 두 set의 교집합을 구하는 함수
def intersection(set1, set2):
    return set1 & set2

# 두 set의 합집합을 구하는 함수
def union(set1, set2):
    return set1 | set2

# Transaction에 포함된 item_set의 개수를 구하는 함수
def get_cnt(item_set):
    cnt = 0
    for trx in transactions:
        if item_set == intersection(item_set, trx): # item_set이 trx의 부분집합인 경우
            cnt += 1
    return cnt

# transaction이 X를 포함할 확률
def get_support(item_set):
    cnt = get_cnt(item_set)
    if cnt >= min_sup_freq: # min_sup 이상인 경우만 구함
        return format((cnt / db_size) * 100, ".2f") 
    else:
        return 0

# X를 포함하는 transaction이 Y도 포함하고 있을 확률
def get_confidence(item_set, associative_itemset):
    X_Y = get_cnt(union(item_set, associative_itemset))
    X = get_cnt(item_set)
    return format((X_Y / X) * 100, ".2f")

# min_sup을 넘지 못하는 itemset을 제거하는 함수
def Pruning(C):
    L = [] # pruning 하고 넣을 배열
    for item_set in C:
        if get_cnt(item_set) >= min_sup_freq: # min_sup 이상인 item_set을 제외하고 pruning
            L.append(item_set)
    return L

# k개의 item으로 이루어진 모든 itemset을 생성
def self_join(itemset, k):
    return list_to_set(list(combinations(itemset, k))) # C_k

# item_set과 associative_item_set을 포함하는 모든 transaction을 찾는 함수
def Apriori():
    k = 1
    candidate = self_join(total_itemset, k) # C_1
    while True:
        L = Pruning(candidate) # L_k
        frequent_pattern.extend(L) 
        if len(L) == 0:
            break
        k += 1
        candidate = self_join(total_itemset, k) # C_k

# association rule을 찾는 함수
def get_associative(item_set):
    global output_file
    if len(item_set) == 1:
        return
    # X -> Y
    X = []
    Y = []

    for i in range(1, len(item_set)):
        X.extend(self_join(item_set, i)) # X의 모든 부분집합
        Y.extend(self_join(item_set, i)) # Y의 모든 부분집합
    
    for prev in X:
        for nxt in Y:
            union_set = union(prev, nxt) # X U Y
            
            support = get_support(union_set) # P(X U Y) 
            confidence = get_confidence(prev, nxt) # P(Y|X)
            
            if support == 0:
                continue
            else:
                line = split_result(make_set(prev), make_set(nxt), str(support), str(confidence))
                output_file.write(line)

def split_result(*line):
    result = ""
    for i in range(len(line)):
        result += line[i] + "\t"
    return result[:-1] + "\n"


def make_set(item_set):
    item_set = sorted(item_set) # {1,2}, {2,1}은 같은 itemset이므로 정렬
    result = "{"
    for item in item_set:
        result += (str(item) + ",")
    return result[:-1] + "}"

# main
output_file = open(sys.argv[3], 'w')
scanDB()
Apriori()

for item_set in frequent_pattern:
    get_associative(item_set)

output_file.close()
