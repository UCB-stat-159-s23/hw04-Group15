from ligotools import readligo
import numpy as np
import os
import fnmatch
import pytest
import json

fnjson = "data/BBH_events_v3.json"
events = json.load(open(fnjson,"r"))
eventname = 'GW150914' 
event = events[eventname]

fn_H1 = event['fn_H1']
fn_L1 = event['fn_L1']

strain_H1, time_H1, chan_dict_H1 = readligo.loaddata("data/"+fn_H1, 'H1')
strain_L1, time_L1, chan_dict_L1 = readligo.loaddata("data/"+fn_L1, 'L1')

strain, gpsStart, ts, qmask, shortnameList, injmask, injnameList = readligo.read_hdf5("data/"+fn_H1)

def test_loaddata_1():
    assert type(strain_L1)==np.ndarray and type(time_L1)==np.ndarray and type(chan_dict_L1)==dict
    assert type(strain_H1)==np.ndarray and type(time_H1)==np.ndarray and type(chan_dict_H1)==dict

def test_loaddata_2():
    assert len(chan_dict_H1) == 13, "incorrect pairs of key and value in the channel dictionary" 
    assert len(chan_dict_L1) == 13, "incorrect pairs of key and value in the channel dictionary" 
    
def test_FileList_list():
    subject = readligo.FileList("./data")
    #assert "data/BBH_events_v3.json" in subject.list
    assert "./data/"+eventname + "_4_template.hdf5" in subject.list
    assert "./data/"+fn_H1 in subject.list
    assert "./data/"+fn_L1 in subject.list

def test_dq_channel_to_seglist():
    seg_L1 = readligo.dq_channel_to_seglist(chan_dict_L1)
    seg_H1 = readligo.dq_channel_to_seglist(chan_dict_H1)
    assert type(seg_L1)==list
    assert type(seg_H1)==list
    
    
    