import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter
import math
from scipy.signal import lfilter
import os

# Purpose
# reads in an audio file

# Params
# path: file path of the input audio

# Returns
# the samples and the sample rate of the file of the given path

def get_samples_and_sample_rate(path):

    sample_rate = -1
    samples = -1
    
    try: 
        sample_rate, samples = wav.read(path)
    except:
        print("Error reading file")    

    return samples, sample_rate

# Purpose 
# saves an audio file given

#  Params
#  path: the file path to name the output file
#  samples: the samples of the audio in which to save
#  sample_rate: the rate at which to sample the output audio

def save_audio(path, samples, sample_rate):
    samples = np.asarray(samples)
    wav.write(path, sample_rate, samples)


# Purpose 
# calculates gain compression on a given audio sample 

#  Params
#  x: the given audio sample value (−32,768 to +32,767)
#  m: the amount to amplify, value >= 1. 
#  compressor_threshold: the point at which to start non-linearly increasing 
#  limiter_threshold: limit of the amplitude 
def calculate_gain_compression(x, m, compresser_threshold, limiter_threshold):

    outputX = x

    # convert compressor threshold and limiter threshold to amplitude
    compresser_threshold_amplitude = math.pow(10, compresser_threshold / 20.0)
    limiter_threshold_amplitude = math.pow(10, limiter_threshold / 20.0)
   
    # linear incrase
    if(x <= compresser_threshold_amplitude):
       outputX = m * x
    
    # non-linear increase (compresion)
    if(x > compresser_threshold_amplitude):
        outputX = m * x + m * x * math.log(x / compresser_threshold_amplitude)
    
    # check if outputX is greater than the limiter threshold
    if(outputX > limiter_threshold_amplitude):
        outputX = limiter_threshold_amplitude

    return outputX

# Purpose 
# to simulate and apply gain compression to a given array of samples

# Params
# samples
# the array of samples

# compressor_threshold: when to start non linear increase (in db)
# limiter_threshold: max amplitude for any value (+ or -) (in db

def apply_gain_compression(compressor_threshold, limiter_threshold):

    samples, sample_rate = get_samples_and_sample_rate("static//audio//output.wav")

    # rows: num of samples
    # cols: num of channels (2)
    rows, cols = samples.shape

    # iterate over each sample using a nested for loop
    for i in range(0, rows):
         for j in range(0, cols):
            samples[i][j] = calculate_gain_compression(samples[i][j], 3, compresser_threshold=compressor_threshold, limiter_threshold=limiter_threshold)
    
    # saves the audio to a new processed audio 
    save_audio("static//audio//processsed_audio.wav", samples, sample_rate)

    os.remove("static//audio//output.wav")
    os.rename("static//audio//processsed_audio.wav", "static//audio//output.wav")

# Purpose
# applies a prep emphasis filter onto given samples
#
# Parameters
#
# Samples 
# the samples of audio provided to apply the filter on
# 
# alpha
# a costant parameter value between 0 and 1
def apply_pre_emphasis_filter(samples, alpha=0):

    # gets the number of samples in the audio samples numpy array provided by the user
    num_samples = len(samples)

    # creates an empty array of zeros with the length of the given audio samples
    y = np.zeros(num_samples)
    
    # applies the formula  y[n] = x[n] – α·x[n-1] given by the project documentation to the samples 
    for x in range(0, num_samples):
        
        y[x] = int(samples[x] - alpha * samples[x - 1])
    
    # converts the array to int16 since audio is 16 bit wav audio
    y = y.astype(np.int16)

    return y  

# Purpose
# 
# applies a low bass butterworth filter to given audio
#
# Params
# filter order: the filter order number provided by the user
#  
# samples: the array of samples provided by the user
#
# sample_rate: sample_rate of the audio provided by the user
#
# returns
# the original audio samples provided by the user with the filter applied

def apply_low_pass_filter(filter_order, samples, sample_rate, cuttoff_freq=10000):

    # butterworth fitler
    # default b type is lowpass
    # 10000 hz is the cutoff frequency as specified by the project outline
    b, a = butter(filter_order, cuttoff_freq, fs=sample_rate)

    # applies the filter to the given audio
    apply_filter = lfilter(b, a, samples)

    # makes the audio samples 16 bit since the wav format is 16 bit wav audio
    apply_filter = apply_filter.astype(np.int16)

    return apply_filter

# Purpose
# 
# apply a butterworth band pass filter with a given pass band
#
# params
# 
# filter_order: the filter order provided by the user
#
# samples: the audio samples provided by the user
# 
# pass band, the pass band with the lower and upper frequencies
#
# returns
# the modified audio with with the applied filter

def apply_bandpass_filter(filter_order, samples, sample_rate, pass_band = [800, 1200]):

    b, a = butter(filter_order, pass_band, fs=sample_rate, btype='bandstop')

     # applies the filter to the given audio
    apply_filter = lfilter(b, a, samples)

    # makes the audio samples 16 bit since the wav format is 16 bit wav audio
    apply_filter = apply_filter.astype(np.int16)

    return apply_filter

# Purpose: To  apply a simple voice-enchancement-like filter consisting of a
#
# 1. Pre-emphasis filter, Implementing the formula y[n] = x[n] – α·x[n-1]
# (with y being the output, x being the input and α between 0 and 1).
#
# 2. Band-pass filter (Butterworth filter, see Lab1), in the range 800-6000 Hz.
# 
# Band-pass filter (Butterworth filter, see Lab1), in the range 800-6000 Hz.
#
# Params
#
# samples: the provided audio samples on which to apply the voice filter
# 
# pre_emphasis_alpha: the alpha value to be used in the formula for the pre-emphasis filter
# 
# high_pass_filter_order: the filter order to use provided by the user
#
# Returns
#
# the samples with the applied simple voice enhancement filter 

def apply_voice_enchancement_filter(samples, sample_rate, pre_emphasis_alpha, high_pass_filter_order):

    samples = apply_pre_emphasis_filter(samples, pre_emphasis_alpha)
    samples = apply_bandpass_filter(high_pass_filter_order, samples, sample_rate, [800, 6000])

    return samples