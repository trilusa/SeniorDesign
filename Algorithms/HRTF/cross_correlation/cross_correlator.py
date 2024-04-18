import pickle
import matplotlib.pyplot as plt
import numpy as np


data = []
hrtf_path = '/home/adrian/Documents/SeniorDesign/BinauralHearingProcessing/SeniorDesign/Algorithms/HRTF/white_noise_data/hrtf_data5.pkl'
with open(hrtf_path, 'rb') as file:
    while True:
        try:
            data.append(pickle.load(file))
        except EOFError:
            break

print(len(data))#[0])

def feature_norm(matrix):
    min_vals = np.min(matrix, axis=1, keepdims=True)
    max_vals = np.max(matrix, axis=1, keepdims=True)
    return (matrix - min_vals) / (max_vals - min_vals)
    # return (v - np.min(v)) / (np.max(v) - np.min(v))

def L2_norm(matrix):
    return matrix / np.linalg.norm(matrix, axis=1, keepdims=True)

hrtf_left = np.array([item[0] for item in data])
hrtf_right = np.array([item[1] for item in data])
angles = np.array([item[2] for item in data])

hrtf_left_norm = L2_norm(hrtf_left)
hrtf_right_norm = L2_norm(hrtf_right)

print(hrtf_left[0])
# m=np.dot(hrtf_left_norm,hrtf_left_norm.T)
m = np.dot(hrtf_left_norm, hrtf_right_norm.T)
plt.plot(np.diagonal(m))
plt.show()
# cross_correlations = np.zeros(len(hrtf_left),len(hrtf_left))
plt.imshow(m, cmap='hot', interpolation='nearest')
plt.colorbar()  # Adds a colorbar to match colors with values
# plt.title('Dot Product Matrix Heatmap')
plt.show()