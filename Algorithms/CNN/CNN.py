import numpy as np
import pandas as pd
from scipy.signal import spectrogram
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, ReLU, Flatten, Dense, Concatenate
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
import time
def compute_spectrogram(data, fs, window_L):
    data=data/(2**15) #normalize
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming', nperseg=window_L, noverlap=window_L//2, nfft=window_L, scaling='density')
    return Sxx

def preprocess_signals(df, window_length,duration):
    inputs = []
    targets = []
    grouped = df.groupby(['az', 'el', 'sound_type', 'sample_rate']) #exppected group size is 2 row
    for _, group in grouped:  
        left_signal = group[group['channel'] == 'L']['signal'].values[0]
        right_signal = group[group['channel'] == 'R']['signal'].values[0]
        sample_rate = group['sample_rate'].values[0]  # Assuming same sample rate for both
        left_spectrogram = compute_spectrogram(left_signal, sample_rate, window_length)[:,:duration]
        right_spectrogram = compute_spectrogram(right_signal, sample_rate, window_length)[:,:duration]
        stacked_spectrograms = np.stack([left_spectrogram, right_spectrogram], axis=-1)  # Expected shape: (256, 200, 2)
        inputs.append(stacked_spectrograms)
        targets.append([group['az'].values[0], group['el'].values[0]])
    inputs = np.array(inputs)
    targets = np.array(targets)
    return inputs, targets
    
def create_cnn_model(input_shape):
    input_layer = Input(shape=input_shape, name='stereo_input')

    # First Convolutional Layer
    x = Conv2D(32, (3, 3), padding='same')(input_layer)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    # Second Convolutional Layer
    x = Conv2D(64, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    # Third Convolutional Layer
    x = Conv2D(128, (3, 3), padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    # Flatten and Dense Output Layer
    x = Flatten()(x)
    predictions = Dense(2, activation='linear')(x)  # Output layer for (az, el)

    # Create and compile the model
    model = Model(inputs=input_layer, outputs=predictions)
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])
    return model

print("\nStarting up\n")
#constants/metaparameters
t_start=time.time(); t_log=[t_start]
window_length = 256 
spectrogram_time_len = 200 #metaparamater
df_file = "/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings.pkl"

#################### Preprocessing ####################
print("**************  Preprocessing *****************")
print(f"  Loading \"{df_file}\"")
df = pd.read_pickle(df_file)
df=df.query('sound_type=="WHITE_NOISE"')
t_log.append(time.time()); 
print(f"Df Loaded: Executed in {t_log[-1]-t_log[-2]} sec\n")

print(f"  Computing Spectrograms...")
inputs, targets = preprocess_signals(df, window_length*2, spectrogram_time_len ) #scipy spectrogram returns below nyquist, so to get 256 we need to pass 512
print(f"Input shape: {inputs.shape}")
print(f"Targets shape: {targets.shape}")
t_log.append(time.time()); print(f"Spectrorams computed: Executed in {t_log[-1]-t_log[-2]} sec\n")

print(f"\Split to train and validation sets...")
X_train, X_val, y_train, y_val = train_test_split(inputs, targets, test_size=0.2, random_state=42)
print("Preprocessing Done!")


# # Assuming inputs is an array of shape [num_samples, 2, 256, 200], and needs reshaping
# inputs = inputs.transpose(0, 2, 3, 1)  # Reshape to [num_samples, 256, 200, 2]
# X_train, X_val, y_train, y_val = train_test_split(inputs, targets, test_size=0.2, random_state=42)
print("************** Model Init **************")
model = create_cnn_model((window_length+1, spectrogram_time_len, 2)) #+1 ro account for DC
model.summary()
t_log.append(time.time()); print(f"Model created: Executed in {t_log[-1]-t_log[-2]} sec\n")
print("Model init done!")

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=32
)
t_log.append(time.time()); print(f"Model trained: Executed in {t_log[-1]-t_log[-2]} sec\n")
print("Model training done!")

print("************** Saving Model **************")
model.save('model_trained_on_whitenoise')
t_log.append(time.time()); print(f"Model saved: Executed in {t_log[-1]-t_log[-2]} sec\n")

print("\nAll done!\n")