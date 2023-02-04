import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":

    df = pd.read_csv(sys.argv[1])
    
    #Q2
    plt.figure()
    plt.plot(df['year'], df['days'])
    plt.xlabel('Year')
    plt.ylabel('Number of frozen days')
    plt.savefig("plot.jpg")

    #Q3a
    X = np.zeros((len(df),2), dtype = int)
    X[:,0] = 1
    X[:,1] = df['year']
    print('Q3a:')
    print(X)

    #Q3b
    Y = np.zeros(len(df), dtype = int)
    Y[:] = df['days']
    print('Q3b:')
    print(Y)
    
    #Q3c
    XT = X.transpose()
    Z = XT.dot(X)
    print('Q3c:')
    print(Z)
    
    #Q3d
    I = np.linalg.inv(Z)
    print('Q3d:')
    print(I)
    
    #Q3e
    PI = I.dot(XT)
    print('Q3e:')
    print(PI)
    
    #Q3f
    hat_beta = PI.dot(Y)
    print("Q3f:")
    print(hat_beta)
    
    #Q4
    y_test = hat_beta[0] + 2021*hat_beta[1]
    print("Q4: " + str(y_test))
    
    #Q5
    if hat_beta[1] < 0:
        print("Q5a: <")
    elif hat_beta[1] == 0:
        print("Q5a: =")
    elif hat_beta[1] > 0:
        print("Q5a: >")
    print("Q5b: This indicates the decrease of freeze days per year as the year" + \
          " increases, subtracting the intercept value with the coefficient times the year")
    
    #Q6
    x_pred = -(hat_beta[0])/hat_beta[1]
    print("Q6a: " + str(x_pred))
    print("Q6b: This sounds reasonable from looking at the data graph; a linear relationship " + \
          "does appear to the eye with the trajectory as x* indicates. A further analysis of the linear"+\
          " regression diagnostics can show if the findings are significant.")



