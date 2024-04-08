import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_data(filename):
    data = []
    with open(filename, 'rb') as file:
        while True:
            try:
                data.append(pickle.load(file))
            except EOFError:
                break
    return data

def plot_hrtf(data):
    # Create a figure and set of subplots
    fig, axs = plt.subplots(len(data), 2, figsize=(10, 5 * len(data)))
    if len(data) == 1:  # Handle the case of a single set of data for subplot indexing
        axs = np.array([axs])

    # Plotting HRTF_left and HRTF_right
    for idx, (hrtf_left, hrtf_right, angle) in enumerate(data):
        if len(data) > 1:
            ax_left = axs[idx, 0]
            ax_right = axs[idx, 1]
        else:
            ax_left = axs[0]
            ax_right = axs[1]

        ax_left.plot(hrtf_left)
        ax_left.set_title(f'HRTF Left - Angle {angle}')
        ax_left.set_xlabel('Frequency Bins')
        ax_left.set_ylabel('Magnitude')

        ax_right.plot(hrtf_right)
        ax_right.set_title(f'HRTF Right - Angle {angle}')
        ax_right.set_xlabel('Frequency Bins')
        ax_right.set_ylabel('Magnitude')

    plt.tight_layout()
    plt.show()

# Load data from pickle file
data = load_data('hrtf_data.pkl')

# Plot the HRTF data
plot_hrtf(data)
