from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    data = np.load(filename)
    center = data - np.mean(data, axis = 0)
    return center

def get_covariance(dataset):
    cov = 1/(len(dataset)-1)*np.dot(np.transpose(dataset), dataset)
    return cov

def get_eig(S, m):
    n = len(S)
    eig, U = eigh(S, subset_by_index=[n-m,n-1])
    sorted2 = np.sort(eig)[::-1]
    diag = np.diag(sorted2)
    U2 = np.fliplr(U)
    return diag, U2

def get_eig_prop(S, prop):
    trace = np.sum(eigh(S, eigvals_only=True))
    minVal = prop*trace
    eig, U = eigh(S, subset_by_value=[minVal,np.inf])
    sorted2 = np.sort(eig)[::-1]
    diag = np.diag(sorted2)
    U2 = np.fliplr(U)
    return diag, U2

def project_image(image, U):
    aij = np.dot(np.transpose(U), image)
    xiPCA = np.dot(U,aij)
    return xiPCA

def display_image(orig, proj):
    matOrig = np.transpose(np.reshape(orig, (32,32)))
    matProj = np.transpose(np.reshape(proj, (32,32)))
    fig, axs = plt.subplots(1,2, figsize=(10, 8))
    axs[0].set_title("Original")
    axs[1].set_title("Projection")
    origImg = axs[0].imshow(matOrig, aspect = 'equal')
    projImg = axs[1].imshow(matProj, aspect = 'equal')
    fig.colorbar(origImg, ax = axs[0], location = 'right', shrink = 0.4675)
    fig.colorbar(projImg, ax = axs[1], location = 'right', shrink = 0.4675)
    plt.show()
    pass
