import numpy as np
import scipy.io.wavfile as wav
import math
import matplotlib.pyplot as plt

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

    print("Sample Rate: ", sample_rate)

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
# limiter_threshold: max amplitude for any value (+ or -) (in db)

# Returns 
# samples with gain compression applied

def apply_gain_compression(samples, compressor_threshold, limiter_threshold):

    for i, sample, in enumerate(samples):

         samples[i] = calculate_gain_compression(sample, 3, compresser_threshold=compressor_threshold, limiter_threshold=limiter_threshold)
    
         
    return samples 

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
def apply_pre_emphasis_filter(samples, alpha=0.9):

    num_samples = len(samples)

    y = [0] * num_samples

    print(num_samples)

    print(len(y))

    for x in range(0, num_samples):
        #print(x)
        
        y[x] = int(samples[x] - alpha * samples[x - 1])

    fig, axs = plt.subplots(2)
    fig.suptitle('Vertically stacked subplots')
    axs[0].plot(y)
    axs[1].plot(samples)

    plt.show()

    return y  