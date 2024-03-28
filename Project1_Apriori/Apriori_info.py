import sys

data = []

def read_data(input_file_path):
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            data.append(list(map(int, line.split())))

def trx_cnt_of_num(number):
    count = 0
    for trx in data:
        if number in trx:
            count += 1
    return count

def get_intersection_cnt(number1, number2):
    count = 0
    for trx in data:
        if number1 in trx and number2 in trx:
            count += 1
    return count
            
def get_total_cnt():
    return len(data)


def main():
    if len(sys.argv) != 5:
        sys.exit(1)
        
    input_file_path = sys.argv[1]
    min_sup = int(sys.argv[2])
    A = int(sys.argv[3])
    B = int(sys.argv[4])
    
    read_data(input_file_path)
    
    total_cnt = get_total_cnt()
    A_trx = trx_cnt_of_num(A)
    B_trx = trx_cnt_of_num(B)
    intersection_cnt = get_intersection_cnt(A, B)
    
    Sup_A = A_trx / total_cnt * 100
    Sup_B = B_trx / total_cnt * 100
    
    AB_conf = intersection_cnt / A_trx * 100
    BA_conf = intersection_cnt / B_trx * 100
    
    print("[Transaction Information]")
    print(f"1. A's transactions count = {A_trx}")
    print(f"2. B's transactions count = {B_trx}")
    print(f"3. Transaction count that contain both A and B = {intersection_cnt}\n")
    
    intersection_sup = min(Sup_A, Sup_B)
    print("[Support Information]")
    if Sup_A >= min_sup and Sup_B >= min_sup:
        print(f"1. Support value of A({A}) : {A_trx} / {total_cnt} = {intersection_sup:.2f}")
        print(f"2. Support value of B({B}) : {B_trx} / {total_cnt} = {intersection_sup:.2f}\n")
    else:
        print(f"1. Support value of A({A}) : {A_trx} / {total_cnt} = {Sup_A:.2f}")
        print(f"2. Support value of B({B}) : {B_trx} / {total_cnt} = {Sup_B:.2f}\n")
        
    
    print("[Confidence Information]")
    print(f"1. Confidence value of AB : {A} -> {B} = {AB_conf:.2f}")
    print(f"2. Confidence value of BA : {B} -> {A} = {BA_conf:.2f}")

if __name__ == "__main__":
    main()
