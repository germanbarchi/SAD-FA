from time import time
import torch
torch.set_num_threads(1)

from IPython.display import Audio
from pprint import pprint
import sys
import os
import glob
import tqdm 
import json
from pathlib import Path 
import pickle
import numpy as np
import soundfile

def timestamps (wav,SAMPLING_RATE):

    # get speech timestamps from full audio file
    speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=SAMPLING_RATE)
    #print(speech_timestamps) 
    
    return speech_timestamps

def save_timestamp(timestamp,ts_parent,ts_out_file):

    if not os.path.exists(ts_parent):            
      os.makedirs(ts_parent)
 
    with open(ts_out_file,'w') as f:
        json.dump(timestamp,f) 

def trim_speech(speech_timestamps,audio_parent,SAMPLING_RATE):
    
    if not os.path.exists(audio_parent):            
      os.makedirs(audio_parent)
      index=0
      
      for i in speech_timestamps: 
        
        start=i['start']
        end=i['end']
        trim=wav[start:end]      
        index+=1
      
        soundfile.write(audio_parent+'/segment_'+str(index)+'.wav',trim,SAMPLING_RATE)

if __name__=='__main__':
    
    cwd=os.getcwd()
    audio=os.path.join(cwd,'audio') 
    
    audio_usr_selection=sys.argv[1] 
    audio_file=audio+'/'+audio_usr_selection+'.wav'  
    
    audio_out_path=os.path.join(cwd,'audio_trimmed/'+audio_usr_selection) 
    ts_path=os.path.join(cwd,'timestamps')        
     
    SAMPLING_RATE = 16000     
    USE_ONNX = False # change this to True if you want to test onnx model

    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                model='silero_vad',
                                force_reload=True,
                                onnx=USE_ONNX)

    (get_speech_timestamps,
    save_audio,
    read_audio,
    VADIterator,
    collect_chunks) = utils 
      
    ts_out_file=os.path.join(ts_path,audio_usr_selection.replace('.wav','.JSON'))
    
    #audio_ns_out_file=os.path.join(audio_ns_path,out)

    #audio_ns_parent=os.path.join(audio_ns_path,part)

    if not os.path.exists(ts_out_file):
                
            wav = read_audio(audio_file, sampling_rate=SAMPLING_RATE)            
            
            tstamps=timestamps(wav,SAMPLING_RATE)            
            
            save_timestamp(tstamps,ts_path,ts_out_file)   
            
            trim_speech(tstamps,audio_out_path,SAMPLING_RATE)

            #non_speech(wav,tstamps,audio_ns_parent,audio_ns_out_file,SAMPLING_RATE)
