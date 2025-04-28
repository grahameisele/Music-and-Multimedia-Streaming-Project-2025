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
# calculates gain compression on a given audio sample 

#  Params
#  x: the given audio sample value (−32,768 to +32,767)
#  m: the amount to amplify, value >= 1. 
#  compressor_threshold: the point at which to start non-linearly increasing 
#  limiter_threshold: limit of the amplitude 
def calculate_gain_compression(x, m, compresser_threshold, limiter_threshold):

    # initialize output x to 0
    outputX = x
    # convert to decibel
    if(x > 0):
        x_in_decibel = 20 * math.log10(abs(x))
    elif(x < 0):
        x_in_decibel = -20 * math.log10(abs(x))
    else:
        x_in_decibel = 0
    
    # linear incrase
    if(x_in_decibel > 0 and x_in_decibel <= compresser_threshold):
       outputX = m * x_in_decibel
    
    # non-linear increase (compresion)
    if(x_in_decibel > compresser_threshold and x_in_decibel > 0):
        outputX = m * x_in_decibel + m * x_in_decibel * math.log(x_in_decibel / compresser_threshold)

    # linear increase
    if(x_in_decibel < 0 and x_in_decibel >= -compresser_threshold):
        outputX = -m * x_in_decibel
    
    # non-linear increase (compresion)
    if(x_in_decibel < 0 and x_in_decibel < -compresser_threshold):
        outputX = -m * compresser_threshold - -m * compresser_threshold * math.log(-x_in_decibel / compresser_threshold)
    
    if(abs(outputX) > limiter_threshold):
        if(outputX) > 0:
            outputX = limiter_threshold
        else:outputX = -limiter_threshold
    
    # convert back to amplitude
    if(x_in_decibel > 0):
        x_in_decibel = math.pow(10, (abs(x_in_decibel) / 20))
    elif(x_in_decibel < 0):
        x_in_decibel = math.pow(10, (abs(x_in_decibel) / 20))
    
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

    # amplitude of 0 is 0 db
    # for each increase in 1 away from 0, increase of db by 0.001497
    for i, sample, in enumerate(samples):

         samples[i] = calculate_gain_compression(sample, 5, compresser_threshold=compressor_threshold, limiter_threshold=limiter_threshold)
    
         
    return samples 
