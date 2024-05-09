import sys
import numpy as np

attributes = []
class_labels = []
training_set = []

class DecisionTree:
    def __init__(self, attribute):
        self.child = dict() # {attribute_value: child_node}
        self.attribute_idx = None
        self.attribute = attribute
        self.class_label = None


    def Info(self, D):
        entropy = 0
        label_values = D.T[-1]

        for label in class_labels:
            p_i = np.sum(label_values == label)/len(D)
            if p_i == 0:
                entropy += 0
            elif p_i > 0:
                entropy += p_i * np.log2(p_i)
        return -entropy


    def Info_A(self, D, A):
        entropy = 0
        attribute_values = np.unique(D.T[A])

        for attribute in attribute_values:
            D_j = D[D.T[A] == attribute]
            if len(D_j) == 0:
                entropy += 0
            elif len(D_j) > 0:
                entropy += (len(D_j)/len(D)) * self.Info(D_j)
        return entropy
    
    
    def Gain(self, D, A):
        return self.Info(D) - self.Info_A(D, A)
    
    
    def SplitInfo(self, D, A):
        result = 0
        attribute_values = np.unique(D.T[A])
        
        for attribute in attribute_values:
            D_j = D[D.T[A] == attribute]
            if len(D_j) == 0:
                result += 0
            elif len(D_j) > 0:
                result += (len(D_j)/len(D)) * np.log2(len(D_j)/len(D))
        return -result
    
    
    def GainRatio(self, D, A):
        splitInfo = self.SplitInfo(D, A)
        Gain = self.Gain(D, A)
        if splitInfo == 0:
            return 0
        elif splitInfo > 0:
            return Gain / splitInfo
    
    
    def MajorityVoting(self, D):
        major_label = None
        max_cnt = 0
        label_values = D.T[-1]
        
        for label in class_labels:
            cnt = np.sum(label_values == label)
            if cnt > max_cnt:
                max_cnt = cnt
                major_label = label
        return major_label
    
    
    def ChooseAttribute(self, D):
        max_info_gain = 0
        target_attribute_idx = None

        for A in range(len(attributes)-1):
            if A in self.attribute: # 이미 사용한 attribute는 제외
                continue
            
            info_gain = self.GainRatio(D, A) 
            
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                target_attribute_idx = A
        return target_attribute_idx
    
    
    def SplitTree(self, D, A): 
        self.attribute_idx = A 
        attribute_values = np.unique(D.T[A])
        
        for attribute in attribute_values:
            D_sub = D[D.T[A] == attribute] # attribute 값에 따라 데이터 분할
            new_branch = DecisionTree(self.attribute.union({A})) # 새로운 노드 생성
            new_branch.Construct(D_sub) # 재귀적으로 트리 생성
            self.child[attribute] = new_branch 


    def Construct(self, D):
        if self.Info(D) == 0: # 모든 데이터가 같은 class label을 가질 때
            self.class_label = D[0][-1] 
            return
        
        self.class_label = self.MajorityVoting(D) # 가장 많은 class label을 가지는 것으로 분류
        if len(self.attribute) == len(attributes) - 1: #모든 attribute를 사용했을 때
            return
        A = self.ChooseAttribute(D) # GainRatio가 가장 큰 attribute 선택
        self.SplitTree(D, A) # 선택한 attribute로 트리 분할


    def Classify(self, D):
        if self.attribute_idx == None:
            return self.class_label
        
        attribute = D[self.attribute_idx]
        if attribute in self.child:  
            return self.child[attribute].Classify(D) # 재귀적으로 분류 (자식 노드로 이동)
        else:
            return self.class_label


def read_input():
    global attributes, class_labels, training_set
    file = open(sys.argv[1], 'r')
    attributes = np.array(file.readline().split())
    while True:
        line = file.readline()
        if not line:
            break
        data = np.array(line.split())
        class_labels.append(data[-1])
        training_set.append(data)
    
    training_set = np.array(training_set)
    class_labels = np.unique(class_labels)

    file.close()


def print_result(D):
    return '\t'.join(str(data) for data in D) + '\n'


def write_output(decision_tree): 
    test_file = open(sys.argv[2], 'r')
    output_file = open(sys.argv[3], 'w')

    test_file.readline()
    output_file.write(print_result(attributes))

    while True:
        line = test_file.readline()
        if not line:
            break
        data = np.array(line.split())

        class_label = decision_tree.Classify(data)
        D = np.append(data, class_label)
        output_file.write(print_result(D))
    
    test_file.close()
    output_file.close()


def main():
    read_input()
    attribute = set()
    decision_tree = DecisionTree(attribute)
    decision_tree.Construct(training_set)
    write_output(decision_tree)


if __name__ == '__main__':
    main()