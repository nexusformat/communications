#!/usr/bin/python
#-------------------------------------------------------------
# A little program to convert SINQ TRICS data files to simulate
# a single photon counting detector file. The
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

txt = 'SPC EIGER'
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

putArrayData(outf,'detector_photon_energy',mils)

txt = 'hugo'
outf.makedata('gate_mode','char',[len(txt)]);
outf.opendata('gate_mode')
outf.putdata(txt)
outf.closedata()

putArrayData(outf,'number_of_excluded_pixels',bitrate)
putArrayData(outf,'summation_n_images',bitrate)
putArrayData(outf,'x_number_of_modules',bitrate)
putArrayData(outf,'y_number_of_modules',bitrate)
putArrayData(outf,'x_number_of_pixels_in_module',bitrate)
putArrayData(outf,'y_number_of_pixels_in_module',bitrate)
putArrayData(outf,'x_number_of_interpixels',bitrate)
putArrayData(outf,'y_number_of_interpixels',bitrate)


txt = 'hugo'
outf.makedata('readout_mode','char',[len(txt)]);
outf.opendata('readout_mode')
outf.putdata(txt)
outf.closedata()

putArrayData(outf,'sub_image_exposure_time',mils)

txt = 'hugo'
outf.makedata('summation_mode','char',[len(txt)]);
outf.opendata('summation_mode')
outf.putdata(txt)
outf.closedata()

txt = 'hugo'
outf.makedata('software_version','char',[len(txt)]);
outf.opendata('software_version')
outf.putdata(txt)
outf.closedata()

txt = 'hugo'
outf.makedata('trigger_mode','char',[len(txt)]);
outf.opendata('trigger_mode')
outf.putdata(txt)
outf.closedata()

outf.makegroup('module1','SPCmodule')
outf.opengroup('module1','SPCmodule')

putArrayData(outf,'x_index',bitrate)
putArrayData(outf,'y_index',bitrate)
putArrayData(outf,'nchips',bitrate)
putArrayData(outf,'nbits',bitrate)


txt = 'hugo'
outf.makedata('daq_names','char',[len(txt)]);
outf.opendata('daq_names')
outf.putdata(txt)
outf.closedata()

ndacs = numpy.ones((8),numpy.dtype('int32'))
putArrayData(outf,'daq_values',ndacs)

txt = 'hugo'
outf.makedata('firmware_version','char',[len(txt)]);
outf.opendata('firmware_version')
outf.putdata(txt)
outf.closedata()

roi = numpy.ones((4),numpy.dtype('int32'))
putArrayData(outf,'region_of_interest',roi)

txt = 'hugo5.dat'
outf.makedata('threshold_calibration_filename','char',[len(txt)]);
outf.opendata('threshold_calibration_filename')
outf.putdata(txt)
outf.closedata()

trim = numpy.ones((64,64),numpy.dtype('int32'))
putArrayData(outf,'trimbit_data',trim)

putArrayData(outf,'rate_correction_lookup_table',trim)

putArrayData(outf,'readout_frequency',mils)



outf.closegroup
outf.closegroup

outf.closegroup()
outf.closegroup()

inf.close()
outf.close()
print 'Done'
