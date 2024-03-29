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
    global db_size, transactions, min_sup, min_sup_freq, total_itemset
    item_list = []
    
    try:
        with open(sys.argv[2], 'r') as input_file:
            for line in input_file:
                trx = list(map(int, line.split()))
                transactions.append(trx)
                for item in trx:
                    item_list.append(int(item))

        db_size = len(transactions)
        total_itemset = set(item_list)
        min_sup_freq = db_size * (min_sup / 100)
        transactions = list_to_set(transactions)
        
    except FileNotFoundError:
        sys.exit(1)

# 중복을 제거하기 위해 set으로 변환
def list_to_set(item_list):
    return [set(item) for item in item_list]

# Transaction에 포함된 item_set의 개수를 구하는 함수
def get_cnt(item_set):
    return sum(1 for trx in transactions if item_set.issubset(trx))

# transaction이 X를 포함할 확률
def get_support(item_set):
    cnt = get_cnt(item_set)
    return format((cnt / db_size) * 100, ".2f") if cnt >= min_sup_freq else '0'

# X를 포함하는 transaction이 Y도 포함하고 있을 확률
def get_confidence(item_set, associative_itemset):
    X_Y = get_cnt(item_set.union(associative_itemset)) # X U Y
    X = get_cnt(item_set) # X
    # division by zero 방지
    if X == 0:
        return '0'
    else:
        return format((X_Y / X) * 100, ".2f") 

# min_sup을 넘지 못하는 itemset을 제거하는 함수
def Pruning(C):
    return [item_set for item_set in C if get_cnt(item_set) >= min_sup_freq]

# k개의 item으로 이루어진 모든 itemset을 생성
def self_join(itemset, k):
    return list_to_set(list(combinations(itemset, k))) # C_k

# item_set과 associative_item_set을 포함하는 모든 transaction을 찾는 함수
def get_associative(item_set, output_file):
    if len(item_set) == 1:
        return
    # X -> Y
    for i in range(1, len(item_set)):
        for prev in self_join(item_set, i): # X
            next_items = item_set.difference(prev) # Y
            support = get_support(prev.union(next_items)) # P(X U Y)
            confidence = get_confidence(set(prev), next_items) # P(Y|X)
            
            if support == '0':
                continue
            else:
                line = split_result(make_itemset(prev), make_itemset(next_items), support, confidence)
                output_file.write(line)

def split_result(item_set, associative_item_set, support, confidence):
    return f"{{{item_set}}}\t{{{associative_item_set}}}\t{support}\t{confidence}\n"

def make_itemset(item_set):
    return ",".join(map(str, sorted(item_set))) # 정렬 후 문자열로 변환

# main
def main():
    output_file = open(sys.argv[3], 'w')
    scanDB()
    
    # Apriori Algorithm
    k = 1
    candidate = self_join(total_itemset, k) # C_1
    while candidate:
        L = Pruning(candidate) # L_k
        frequent_pattern.extend(L) # frequent_pattern에 추가
        k += 1
        candidate = self_join(total_itemset, k) # C_k

    for item_set in frequent_pattern:
        get_associative(item_set, output_file)

    output_file.close()

if __name__ == "__main__":
    main()
