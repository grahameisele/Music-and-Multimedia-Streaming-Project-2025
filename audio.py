import numpy as np
import scipy.io.wavfile as wav
import math


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
# to simulate and apply gain compression to a given array of samples

# Params
# samples
# the array of samples

# Returns 
# samples with gain compression applied

def apply_gain_compression(samples):

    for i, sample, in enumerate(samples):

        if sample > 0:
            samples[i] = (abs(sample) + 1000 * math.sqrt(sample)) / 6.0

        if sample < 0:
            samples[i] = -1.0 * ((abs(sample) + 1000 * math.sqrt(abs(sample))) / 6.0)

        if samples[i] > 32767:
            samples[i] = 32767
        
        if samples[i] < -32768:
            samples[i] = 32768
    
    return samples 
