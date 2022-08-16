import pandas as pd 
import sys
import librosa
import soundfile
import os

def trim_audio(y,fs,df,out_path):

    for i in range(df.shape[0]):
        
        start=int(df.iloc[i]['start']*fs)
        end=int(df.iloc[i]['stop']*fs)
        filename=df.iloc[i]['name']
        trim=y[start:end]

        soundfile.write(out_path+'/'+filename+'.wav',trim,fs)

if __name__=='__main__':

    timestamps_df=sys.argv[1]    
    audio=sys.argv[2]
    out_path=sys.argv[3]
    list_name=sys.argv[4]

    df=pd.read_csv(timestamps_df)
    
    out_path=out_path+'/'+list_name
    
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    y,fs=librosa.core.load(audio,sr=None)

    trim_audio(y,fs,df,out_path)