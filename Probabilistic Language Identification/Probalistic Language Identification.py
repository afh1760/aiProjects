import sys
import math
from string import ascii_uppercase

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()
    with open (filename,encoding='utf-8') as f:
        for i in ascii_uppercase:
            X[i] = 0
        for line in f:
            for j in line.upper():
                if j in ascii_uppercase:
                    X[j] = X.get(j,0)+1
    return X

print("Q1")
X = shred('letter.txt')
for key,value in X.items():
    print(key, value)
    
print("Q2")
e,s = get_parameter_vectors()
X_list = list(X.values())
e2 = round(X_list[0]*math.log(e[0]),4)
print(f'{e2:.4f}')
s2 = round(X_list[0]*math.log(s[0]),4)
print(f'{s2:.4f}')

print("Q3")
sum_e = 0
sum_s = 0
for i in range(26):
    sum_e += (X_list[i]*math.log(e[i]))
    sum_s += (X_list[i]*math.log(s[i]))   
F_e = round(math.log(0.6) + sum_e,4)
F_s = round(math.log(0.4) + sum_s,4)           
print(f'{F_e:.4f}')
print(f'{F_s:.4f}')

print("Q4")
P_e = round(1/(1+math.exp(F_s - F_e)),4)
print(f'{P_e:.4f}')
