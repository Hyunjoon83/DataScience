# Project2 : Decision Tree

## Decision Tree Algorithm

![image](https://github.com/Hyunjoon83/DataScience/assets/141709404/49289603-2dd4-4364-bcb5-69fb800181b5)
![image](https://github.com/Hyunjoon83/DataScience/assets/141709404/5c828e69-da5c-4977-9c6f-4291c449eb92)

### ID3 (Iterative Dichotomiser 3)

- $Info(D)=-\Sigma_{i=1}^{m}p_i log_2(p_i)$
  
- $Info_A(D) = \Sigma_{j=1}^v{{|D_j|}\over{|D|}}Info(D_j)$
  
- $Gain(A) = Info(D) - Info_A(D)$

#### Code

```python
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
```


### C4.5

- $SplitInfo_A(D) = -\Sigma_{j=1}^v{{|D_j|}\over{|D|}}log_2({{|D_j|}\over{|D|}})$

- $GainRatio(A) = Gain(A) / SplitInfo_A(D)$

#### Code
```python
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
```

## Files

### 1. [dt.py](https://github.com/Hyunjoon83/DataScience/blob/main/Project2_Decision_Tree/dt.py)

: main_code

### 2. Result
1) ```python dt.py dt_train1.txt dt_test1.txt dt_result1.txt```
   
   ```dt_test.exe dt_answer1.txt dt_result1.txt```
   
2) ```python dt.py dt_train.txt dt_test.txt dt_result.txt```
   
   ```dt_test.exe dt_answer.txt dt_result.txt```
   
![image](https://github.com/Hyunjoon83/DataScience/assets/141709404/78dd369e-80f9-4246-aca9-3f83932642a0)
