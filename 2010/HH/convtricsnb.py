#!/usr/bin/python
#-------------------------------------------------------------
# A little program to convert SINQ TRICS data files to adhere
# to the NXxnb application definition.
#
# copyright: Do not even consider to bother me
#
# Mark Koennecke, July 2009
#-------------------------------------------------------------

#------ Python blabla where it finds its stuff......
import sys
sys.path.append('/afs/psi.ch/project/sinq/sl5/lib/python')
sys.path.append('/afs/psi.ch/project/sinq/sl5/lib/python2.4/site-packages')

import nxs,numpy


if len(sys.argv) < 3:
    print "Usage:\n\tconvtricsnb.py infile outfile"
    sys.exit(0)

def makeLooser(infile, outfile):
    outfile.makegroup('user','NXuser')
    outfile.opengroup('user','NXuser')
    numatt = infile.getattrinfo()
    for i in range(numatt):
        name,dims,type = infile.getnextattr()
        if name == 'owner':
            data = infile.getattr(name,dims,type)
            outfile.makedata('name','char',[dims])
            outfile.opendata('name')
            outfile.putdata(data)
            outfile.closedata()
        if name == 'owner_address':
            data = infile.getattr(name,dims,type)
            outfile.makedata('address','char',[dims])
            outfile.opendata('address')
            outfile.putdata(data)
            outfile.closedata()
        if name == 'owner_email':
            data = infile.getattr(name,dims,type)
            outfile.makedata('email','char',[dims])
            outfile.opendata('email')
            outfile.putdata(data)
            outfile.closedata()
        if name == 'owner_telephone_number':
            data = infile.getattr(name,dims,type)
            outfile.makedata('telephone_number','char',[dims])
            outfile.opendata('telephone_number')
            outfile.putdata(data)
            outfile.closedata()
        if name == 'owner_fax_number':
            data = infile.getattr(name,dims,type)
            outfile.makedata('fax_number','char',[dims])
            outfile.opendata('fax_number')
            outfile.putdata(data)
            outfile.closedata()
    outfile.closegroup()

def copyData(infile, inpath, outfile, outname):
    infile.openpath(inpath)
    shape,dtype = infile.getinfo()
    outfile.makedata(outname,dtype,shape)
    outfile.opendata(outname)
    data = infile.getdata()
    outfile.putdata(data)
    outfile.closedata()


def makeStink(outf, targetpath, topath):
    outf.openpath(targetpath)
    id = outf.getdataID()
    outf.openpath(topath)
    outf.makelink(id)

inf = nxs.open(sys.argv[1],'r')
outf = nxs.open(sys.argv[2],'w5')
outf.makegroup('entry','NXentry')
outf.opengroup('entry','NXentry')

makeLooser(inf,outf)

copyData(inf,'/entry1/title', outf,'title')
copyData(inf,'/entry1/start_time', outf,'start_time')
copyData(inf,'/entry1/end_time', outf,'end_time')
data = 'NXxnb'
outf.makedata('definition','char',[len(data)]);
outf.opendata('definition')
outf.putdata(data)
data = 'http://svn.nexusformat.org/definitions/NXxnb.nxdl.xml'
outf.putattr('URL',data)
outf.closedata()


#------------- sample
outf.makegroup('sample','NXsample')
outf.opengroup('sample','NXsample')
copyData(inf,'/entry1/sample/name',outf,'name')
copyData(inf,'/entry1/sample/rotation_angle',outf,'rotation_angle')
copyData(inf,'/entry1/sample/UB',outf,'orientation_matrix')
copyData(inf,'/entry1/sample/cell',outf,'unit_cell')
try:
    copyData(inf,'/entry1/sample/temperature',outf,'temperature')
except:
    outf.makedata('temperature','float32',[1]);
    outf.opendata('temperature')
    outf.putdata(-999.99)
    outf.closedata()
    
outf.closegroup()

#-------- control
outf.makegroup('control','NXmonitor')
outf.opengroup('control','NXmonitor')
copyData(inf,'/entry1/control/data',outf,'data')
copyData(inf,'/entry1/control/mode',outf,'mode')
copyData(inf,'/entry1/control/preset',outf,'preset')
copyData(inf,'/entry1/control/time',outf,'time')
outf.closegroup()


#--------- Instrument
outf.makegroup('instrument','NXinstrument')
outf.opengroup('instrument','NXinstrument')
data = 'TRICS'
outf.makedata('name','char',[len(data)]);
outf.opendata('name')
outf.putdata(data)
outf.closedata()


#-------- NXsource
outf.makegroup('source','NXsource')
outf.opengroup('source','NXsource')
copyData(inf,'/entry1/TRICS/SINQ/name',outf,'name')
data = 'neutron'
outf.makedata('probe','char',[len(data)])
outf.opendata('probe')
outf.putdata(data)
outf.closedata()
data = 'Spallation Neutron Source'
outf.makedata('type','char',[len(data)])
outf.opendata('type')
outf.putdata(data)
outf.closedata()
outf.closegroup() 

#------------ NXmonochromator
outf.makegroup('monochromator','NXmonochromator')
outf.opengroup('monochromator','NXmonochromator')
copyData(inf,'/entry1/TRICS/monochromator/wavelength',outf,'wavelength')
outf.closegroup() 

#---------- Detector
outf.makegroup('detector','NXdetector')
outf.opengroup('detector','NXdetector')
copyData(inf,'/entry1/TRICS/area_detector2/data',outf,'data')
copyData(inf,'/entry1/TRICS/area_detector2/distance',outf,'distance')
outf.opendata('data')
outf.putattr('signal',1,dtype='int32')
outf.closedata()
copyData(inf,'/entry1/TRICS/area_detector2/x_pixel_size',outf,'x_pixel_size')
copyData(inf,'/entry1/TRICS/area_detector2/y_pixel_size',outf,'y_pixel_size')
copyData(inf,'/entry1/TRICS/area_detector2/polar_angle',outf,'polar_angle')
copyData(inf,'/entry1/TRICS/area_detector2/tilt_angle',outf,'tilt_angle')

outf.closegroup

outf.closegroup()
outf.closegroup()

#------------- NXdata
outf.makegroup('data','NXdata')
outf.opengroup('data','NXdata')
outf.closegroup()
outf.closegroup()
makeStink(outf,'/entry/instrument/detector/data','/entry/data')
makeStink(outf,'/entry/instrument/detector/polar_angle','/entry/data')
makeStink(outf,'/entry/instrument/detector/tilt_angle','/entry/data')
makeStink(outf,'/entry/sample/rotation_angle','/entry/data')

inf.close()
outf.close()
print 'Done'
