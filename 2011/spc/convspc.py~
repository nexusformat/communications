#!/usr/bin/python
#-------------------------------------------------------------
# A little program to convert SINQ TRICS data files to simulate
# a single photon counting detector file for DECTRIS. The
# assumed detector size is 256x128, the number of frames 101.
#
# Consider all number as useless
#
# copyright: Do not even consider to bother me
#
# Mark Koennecke, December 2011
#-------------------------------------------------------------

#------ Python blabla where it finds its stuff......
import sys
sys.path.append('/afs/psi.ch/project/sinq/sl5/lib/python')
sys.path.append('/afs/psi.ch/project/sinq/sl5/lib/python2.4/site-packages')

import nxs,numpy


if len(sys.argv) < 3:
    print "Usage:\n\tconvdectris.py infile outfile"
    sys.exit(0)


def putArrayData(outf,name, ardata):
    outf.makedata(name,ardata.dtype.name,ardata.shape)
    outf.opendata(name)
    outf.putdata(ardata)
    outf.closedata()

def copyData(infile, inpath, outfile, outname):
    infile.openpath(inpath)
    shape,dtype = infile.getinfo()
    outfile.makedata(outname,dtype,shape)
    outfile.opendata(outname)
    data = infile.getdata()
    outfile.putdata(data)
    outfile.closedata()

inf = nxs.open(sys.argv[1],'r')
outf = nxs.open(sys.argv[2],'w5')
outf.makegroup('entry','NXentry')
outf.opengroup('entry','NXentry')


#--------- Instrument
outf.makegroup('instrument','NXinstrument')
outf.opengroup('instrument','NXinstrument')

#---------- Detector
outf.makegroup('detector','NXdetector')
outf.opengroup('detector','NXdetector')
copyData(inf,'/entry1/TRICS/area_detector2/data',outf,'data')
copyData(inf,'/entry1/TRICS/area_detector2/distance',outf,'distance')
outf.opendata('data')
outf.putattr('signal',1,dtype='int32')
outf.closedata()

data = numpy.ones((256,128),numpy.dtype('float32'))
putArrayData(outf,'x_pixel_offset',data)
putArrayData(outf,'y_pixel_offset',data)
putArrayData(outf,'x_pixel_size',data)
putArrayData(outf,'y_pixel_size',data)

txt = 'DECTRIS EIGER'
outf.makedata('type','char',[len(txt)]);
outf.opendata('type')
outf.putdata(txt)
outf.closedata()


txt = 'gated'
outf.makedata('acquisition_mode','char',[len(txt)]);
outf.opendata('acquisition_mode')
outf.putdata(txt)
outf.closedata()

flag = numpy.ones((1),numpy.dtype('int32'))
putArrayData(outf,'angular_calibration_applied',flag)
putArrayData(outf,'angular_calibration',data)

putArrayData(outf,'flatfield_applied',flag)
putArrayData(outf,'flatfield',data)
putArrayData(outf,'flatfield_error',data)

data = numpy.ones((256,128),numpy.dtype('int32'))
putArrayData(outf,'pixelmask_applied',flag)
putArrayData(outf,'pixelmask',data)

putArrayData(outf,'countrate_correction_applied',flag)

bitrate = numpy.ones((1),numpy.dtype('int32'))
putArrayData(outf,'bit_dpeth_readout',bitrate)

mils = numpy.ones((1),numpy.dtype('float32'))
mils[0] = 26
putArrayData(outf,'detector_readout_time',mils)
putArrayData(outf,'trigger_delay_time',mils)
putArrayData(outf,'trigger_dead_time',mils)

npdata = numpy.ones((101),numpy.dtype('float32'))
putArrayData(outf,'frame_time',npdata)
putArrayData(outf,'count_time',npdata)


txt = 'high'
outf.makedata('gain_setting','char',[len(txt)]);
outf.opendata('gain_setting')
outf.putdata(txt)
outf.closedata()

putArrayData(outf,'saturation_value',flag)
putArrayData(outf,'number_of_cyles',flag)

txt = 'silicon'
outf.makedata('sensor_material','char',[len(txt)]);
outf.opendata('sensor_material')
outf.putdata(txt)
outf.closedata()

putArrayData(outf,'sensor_thickness',mils)
putArrayData(outf,'threshold_energy',mils)



outf.closegroup

outf.closegroup()
outf.closegroup()

inf.close()
outf.close()
print 'Done'
