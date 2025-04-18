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


def calculate_gain_compression(x, m, compresser_threshold=0, limiter_threshold=49.05):
    
    #convert to decibel
    newX = x * 0.001497
    
    if(x > 0 and x <= compresser_threshold):
       newX = m * x
    
    if(x > compresser_threshold and x <= 49.05):
        newX = m * x + m * x * math.log(x / compresser_threshold)

    if(x >= 0 and x >= -compresser_threshold):
        newX = m * x
    
    if(x >= -49 and x < -compresser_threshold):
        -m * compresser_threshold - -m * compresser_threshold * math.log(-x / compresser_threshold)
    
    if(abs(newX) > limiter_threshold):
        if(newX) > 0:
            newX = limiter_threshold
        else:newX = -limiter_threshold
    
    # convert back to integer
    newX = round(newX / 0.001497)
    return newX

# Purpose 
# to simulate and apply gain compression to a given array of samples

# Params
# samples
# the array of samples

# compressor_threshold: when to start non linear increase (in db)
# limiter_threshold: max amplitude for any value (+ or -) (in db)

# Returns 
# samples with gain compression applied

def apply_gain_compression(samples, compressor_threshold=0, limiter_threshold=49.05):

    # amplitude of 0 is 0 db
    # for each increase in 1 away from 0, increase of db by 0.001497
    for i, sample, in enumerate(samples):

         samples[i] = calculate_gain_compression(sample, 1.01, compresser_threshold=compressor_threshold, limiter_threshold=limiter_threshold)
    
    return samples 
