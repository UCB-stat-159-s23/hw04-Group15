from ligotools import readligo
import numpy as np

file_L1 = "data/L-L1_LOSC_4_V2-1126259446-32.hdf5"
file_H1 = "data/H-H1_LOSC_4_V2-1126259446-32.hdf5"


strain_L1, meta_L1, channel_dict_L1 = readligo.loaddata(file_L1)
strain_H1, meta_H1, channel_dict_H1 = readligo.loaddata(file_H1)
strain, gpsStart, ts, qmask, shortnameList, injmask, injnameList = rl.read_hdf5(file_H1)

def test_loaddata():
    assert type(strain_L1)==np.ndarray and type(meta_L1)==np.darray and type(channel_dict_L1)==dict
    assert type(strain_H1)==np.ndarray and type(meta_H1)==np.darray and type(channel_dict_H1)==dict
    
def test_read_hdf5_and_dq2segs():
    assert gpsStart!=None
    
    seglist = readligo.dq2segs(channel_dict_H1, gpsStart)
    assert seglist!=None
    
def test_dq_channel_to_seglist():
    seg_L1 = readligo.dq_channel_to_seglist(channel_dict_L1)
    seg_H1 = readligo.dq_channel_to_seglist(channel_dict_H1)
    
    assert type(seg_L1)==list
    assert type(seg_H1)==list
    
def test_SegmentList():
    subject = readligo.SegmentList(file_L1)
    assert subject.list!=None
    
    start = subject.seglist[0][0]
    stop = subject.seglist[0][1]
    assert isinstance(readligo.getsegs(start, stop, None), readligo.SegmentList)
    
    
    