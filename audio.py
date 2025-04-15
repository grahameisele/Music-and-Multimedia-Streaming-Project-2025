import numpy as np
import scipy.io.wavfile as wav
import math


# Purpose
# reads in an audio file given an input file path

# Params
# path: file path of the input audio

# Returns
# the samples and the sample rate of the file of the given path

def get_samples_and_sample_rate(path):

    sample_rate = -1
    samples = -1
    
    try: 
        sample_rate, samples = wav.read(path)
        samples = samples.astype(np.float32) 
    except:
        print("Error reading file")    

    return [samples, sample_rate]

# Purpose
# adds gain compression to a given audio 

# Params
# samples: the array of samples of a given audio file
# sample_rate: the sample rate of the given audio file
# alpha: an adjustable parameter to change how much to increase distortion 

def add_gain_compression(samples, alpha=1):

    samples_min = np.min(samples)

    for i, sample in enumerate(samples):
        delta = sample - samples_min
        try:
            if delta > 0:
                samples[i] = (1 + (alpha / math.log10(delta)))
            else:
                samples[i] = 1  # Or some default value to avoid distortion
        except Exception as error:
            print("current sample:", sample)
            print("sample min:", samples_min)
            print("delta:", delta)
            print("An exception occurred:", error)
    
    return samples

