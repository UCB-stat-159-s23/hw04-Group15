from ligotools import readligo
from ligotools import utils
import numpy as np
import matplotlib.mlab as mlab
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import h5py
import json

from scipy.io import wavfile

fnjson = "data/BBH_events_v3.json"
events = json.load(open(fnjson,"r"))
eventname = 'GW150914' 
event = events[eventname]

fn_H1 = event['fn_H1']
fn_L1 = event['fn_L1']
fs = event['fs']
fband = event['fband']

strain_H1, time_H1, chan_dict_H1 = readligo.loaddata("data/"+fn_H1, 'H1')
strain_L1, time_L1, chan_dict_L1 = readligo.loaddata("data/"+fn_L1, 'L1')

NFFT = 4*fs
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
Pxx_L1, freqs = mlab.psd(strain_L1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
psd_L1 = interp1d(freqs, Pxx_L1)

time = time_H1 # H1 and L1 share the same time vector
dt =  time[1]-time[0] 

# create H1 and L1 whiten file
strain_H1_whiten = utils.whiten(strain_H1, psd_H1, dt)
strain_L1_whiten = utils.whiten(strain_L1, psd_L1, dt)

# suppress the high frequency noise
bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
strain_H1_whitenbp = filtfilt(bb, ab, strain_H1_whiten) / normalization
strain_L1_whitenbp = filtfilt(bb, ab, strain_L1_whiten) / normalization

tevent = event['tevent']
deltat_sound = 2
indxd = np.where((time >= tevent-deltat_sound) & (time < tevent+deltat_sound))
# write H1 and L1 whiten wavfile
wavfile_H1 = utils.write_wavfile("audio/"+eventname+"_H1_whitenbp.wav",int(fs), strain_H1_whitenbp[indxd])
wavfile_L1 = utils.write_wavfile("audio/"+eventname+"_L1_whitenbp.wav",int(fs), strain_L1_whitenbp[indxd])

def test_whiten():
    assert strain_H1_whiten is not None
    assert strain_L1_whiten is not None
    # add more tests for whiten
    
def test_write_wavfile():
    audio_list = ["GW150914_H1_shifted.wav",
                 "GW150914_H1_whitenbp.wav",
                 "GW150914_L1_shifted.wav",
                 "GW150914_L1_whitenbp.wav",
                 "GW150914_template_shifted.wav",
                 "GW150914_template_whiten.wav"]
    assert eventname+"_H1_whitenbp.wav" in audio_list # test if the wavfile is created or not
    assert eventname+"_L1_whitenbp.wav" in audio_list
    
def test_reqshift_1():
    fs = 4096
    fshift = 400
    reqshift_H1 = utils.reqshift(strain_H1_whitenbp, fshift, fs)
    reqshift_L1 = utils.reqshift(strain_L1_whitenbp, fshift, fs)
    assert reqshift_H1 is not None
    assert reqshift_L1 is not None

def tests_reqshift_2():
    fs = 4096
    fshift = 400
    reqshift_H1 = utils.reqshift(strain_H1_whitenbp, fshift, fs)
    reqshift_L1 = utils.reqshift(strain_L1_whitenbp, fshift, fs)
    assert type(reqshift_H1) == np.ndarray 
    assert type(reqshift_L1) == np.ndarray
    