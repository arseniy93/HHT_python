import numpy as np
import matplotlib.pyplot as plt
from PyEMD import EMD,EEMD,CEEMDAN
from scipy.signal import hilbert, stft, cwt, ricker,morlet2
from scipy.fft import fft, fftfreq

# 1. Define the sampling parameters

fs = 8000  # Sampling frequency in Hz
T = 1  # Duration in seconds
t = np.linspace(0, T, fs * T, endpoint=False)  # Time vector

# 2. Define the signal
signal = (
    2*np.sin(2 * np.pi*3500*t)+np.sin(2 * np.pi*1500*t)+np.sin(t*2 * np.pi*1000)+np.sin(t*2 * np.pi*1050)+np.sin(t*2 * np.pi*1100)+5*np.sin(2 * np.pi*2500*t)

    # np.sin(2 * np.pi * 10 * t)+ np.sin(2 * np.pi * 100 * t)+ np.sin(2 * np.pi * 4500 * t)
        # (1 + 0.3  * np.sin(2 * np.pi * 15 * t)) *
        # np.cos(2 * np.pi * 60 * t + 0.5 * np.sin(2 * np.pi * 30 * t)) +
        # np.sin(2 * np.pi * 200 * t)
)

# 3. Plot the original signal
plt.figure(figsize=(12, 4))
plt.plot(t, signal, label='Original Signal')
plt.title('Original Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. Perform Empirical Mode Decomposition (EMD)
emd = EMD()
IMFs = emd.emd(signal, t)
num_imfs = IMFs.shape[0]
print(f'Number of IMFs: {num_imfs}')

# 5. Plot the IMFs
# plt.figure(figsize=(12, 2 * num_imfs))
# for i in range(num_imfs):
#     plt.subplot(num_imfs, 1, i + 1)
#     plt.plot(t, IMFs[i], label=f'IMF {i + 1}')
#     plt.title(f'IMF {i + 1}')
#     plt.xlabel('Time [s]')
#     plt.ylabel('Amplitude')
#     plt.legend()
#     plt.grid(True)
# plt.tight_layout()
# plt.show()

# 6. Apply Hilbert Transform to each IMF to get instantaneous amplitude and frequency
inst_amplitudes = []
inst_frequencies = []

for i in range(num_imfs):
    analytic_signal = hilbert(IMFs[i])
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_freq = (np.diff(instantaneous_phase) / (2.0 * np.pi)) * fs  # Convert to Hz
    instantaneous_freq = np.insert(instantaneous_freq, 0, instantaneous_freq[0])  # Maintain length
    inst_amplitudes.append(amplitude_envelope)
    inst_frequencies.append(instantaneous_freq)


# 7. Plot Instantaneous Amplitude and Frequency for each IMF
# for i in range(num_imfs):
#     fig, axs = plt.subplots(2, 1, figsize=(12, 6))
#
#     # Instantaneous Amplitude
#     axs[0].plot(t, inst_amplitudes[i], label=f'IMF {i + 1} Amplitude')
#     axs[0].set_title(f'IMF {i + 1} - Instantaneous Amplitude')
#     axs[0].set_xlabel('Time [s]')
#     axs[0].set_ylabel('Amplitude')
#     axs[0].legend()
#     axs[0].grid(True)
#
#     # Instantaneous Frequency
#     axs[1].plot(t, inst_frequencies[i], label=f'IMF {i + 1} Frequency')
#     axs[1].set_title(f'IMF {i + 1} - Instantaneous Frequency')
#     axs[1].set_xlabel('Time [s]')
#     axs[1].set_ylabel('Frequency [Hz]')
#     axs[1].legend()
#     axs[1].grid(True)
#
#     plt.tight_layout()
#     plt.show()

# 8. Compute the Marginal Spectrum
# Define frequency bins
freq_bins = np.linspace(0, fs / 2, fs // 2 + 1)  # Up to Nyquist frequency

# Initialize the marginal spectrum
marginal_spectrum = np.zeros_like(freq_bins)

# Accumulate the amplitude contributions
for i in range(num_imfs):
    amp = inst_amplitudes[i]
    freq = inst_frequencies[i]

    # Bin the instantaneous frequencies
    epsilon = 1e-6  # Small value to prevent indexing errors
    freq_binned = np.digitize(freq + epsilon, freq_bins) - 1  # Zero-based indexing

    # Ensure indices are within valid range
    freq_binned = np.clip(freq_binned, 0, len(freq_bins) - 1)

    # Accumulate the amplitudes
    for j in range(len(amp)):
        marginal_spectrum[freq_binned[j]] += amp[j]

# Normalize the marginal spectrum
marginal_spectrum /= np.max(marginal_spectrum)

# 9. Plot the Marginal Spectrum
plt.figure(figsize=(12, 6))
plt.plot(freq_bins, marginal_spectrum, color='blue', linewidth=1.5)
plt.title('Marginal Spectrum of the Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Normalized Magnitude')
plt.xlim(0, fs )  # Focus on frequencies up to 300 Hz for clarity
plt.grid(True)

# Highlight expected frequencies
plt.axvline(x=15, color='orange', linestyle='--', label='15 Hz')
plt.axvline(x=60, color='red', linestyle='--', label='60 Hz')
plt.axvline(x=200, color='green', linestyle='--', label='200 Hz')
plt.legend()
plt.tight_layout()
plt.show()
#-----------------------------------------------------------------------------------------------------
# 10. Short-Time Fourier Transform (STFT)
f, t_stft, Zxx = stft(signal, fs, nperseg=1024, noverlap=512)
plt.figure(figsize=(12, 6))
plt.pcolormesh(t_stft, f, np.abs(Zxx), shading='gouraud', cmap='viridis')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar(label='Magnitude')
plt.ylim(0, fs / 2)
plt.tight_layout()
plt.show()

# 11. Continuous Wavelet Transform (CWT) with Morlet wavelet
widths = np.arange(1, 257)  # Scale range
cwtmatr = cwt(signal, morlet2, widths, w=5.0) # Используем morlet2, w - параметр формы

# Calculate pseudo-frequencies
sampling_period = T / len(signal)
frequencies = (widths * fs) / (2 * np.pi * 5.0 * sampling_period)  # Approximation of scale-to-frequency

plt.figure(figsize=(12, 6))
plt.imshow(
    abs(cwtmatr),
    extent=[t.min(), t.max(), frequencies[-1], frequencies[0]],
    cmap="viridis",
    aspect="auto",
    vmax=abs(cwtmatr).max(),
    vmin=-abs(cwtmatr).max(),
)
plt.title("CWT Magnitude (Morlet)")
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [sec]")
plt.colorbar(label="Magnitude")
plt.ylim(0, fs / 2)  # Limit y-axis to Nyquist frequency
plt.tight_layout()
plt.show()

# 12. Calculate the FFT of the signal
yf = fft(signal)
xf = fftfreq(len(signal), 1 / fs)

# Take the absolute value to get the magnitude spectrum
magnitude_spectrum = np.abs(yf)

# 13. Plot the frequency spectrum
plt.figure(figsize=(12, 6))
plt.plot(xf, magnitude_spectrum, color='blue', linewidth=1.5)
plt.title('Frequency Spectrum of the Signal (FFT)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.xlim(0, fs/2)  # Limit to the Nyquist frequency
plt.grid(True)
plt.tight_layout()
plt.show()

# 5. Plot the IMFs
# plt.figure(figsize=(12, 2 * num_imfs))
# for i in range(num_imfs):
#     yf = fft(signal)
#     xf = fftfreq(len(signal), 1 / fs)
#     plt.subplot(num_imfs, 1, i + 1)
#     plt.plot(xf, yf, label=f'IMF {i + 1}')
#     plt.title(f'IMF {i + 1}')
#     plt.xlabel('Time [s]')
#     plt.ylabel('Amplitude')
#     plt.legend()
#     plt.grid(True)
# plt.tight_layout()
# plt.show()

