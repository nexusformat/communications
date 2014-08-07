#!/usr/bin/python
#-------------------------------------------------------------
# A little program to convert SINQ SANS data files to adhere
# to the NXsanssax application definition.
#
# copyright: Do not even consider to bother me
#
# Mark Koennecke, June 2009
#
# Updated for better SAS definition
#
# Mark Koennecke, July 2010
#-------------------------------------------------------------

#------ Python blabla where it finds its stuff......
import sys
sys.path.append('/afs/psi.ch/project/sinq/sl5/lib/python')
sys.path.append('/afs/psi.ch/project/sinq/sl5/lib/python2.4/site-packages')

import nxs,numpy


if len(sys.argv) < 3:
    print "Usage:\n\tconvsans.py infile outfile"
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

def writeAngle(outf,name, value):
    data = numpy.array([value], numpy.float32)
    outf.makedata(name,'float32',[len(data)])
    outf.opendata(name)
    outf.putdata(data)
    outf.closedata()

    

inf = nxs.open(sys.argv[1],'r')
outf = nxs.open(sys.argv[2],'w5')
outf.makegroup('entry','NXentry')
outf.opengroup('entry','NXentry')

makeLooser(inf,outf)

copyData(inf,'/entry1/title', outf,'title')
copyData(inf,'/entry1/start_time', outf,'start_time')
copyData(inf,'/entry1/end_time', outf,'end_time')
data = 'NXsanssax'
outf.makedata('definition','char',[len(data)]);
outf.opendata('definition')
outf.putdata(data)
data = 'http://svn.nexusformat.org/definitions/NXsanssax.nxdl.xml'
outf.putattr('URL',data)
outf.closedata()


#------------- sample
outf.makegroup('sample','NXsample')
outf.opengroup('sample','NXsample')
writeAngle(outf,'aequatorial_angle',0)
copyData(inf,'/entry1/sample/name',outf,'name')
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
copyData(inf,'/entry1/SANS/detector/monitor_counts',outf,'data')
copyData(inf,'/entry1/SANS/detector/count_mode',outf,'mode')
copyData(inf,'/entry1/SANS/detector/preset',outf,'preset')
copyData(inf,'/entry1/SANS/detector/counting_time',outf,'count_time')
outf.closegroup()

#outf.makegroup('beam','NXmonitor')
#outf.opengroup('beam','NXmonitor')
#copyData(inf,'/entry1/DMC/DMC-BF3-Detector/beam_monitor',outf,'data')
#outf.closegroup()

#--------- Instrument
outf.makegroup('instrument','NXinstrument')
outf.opengroup('instrument','NXinstrument')
copyData(inf,'/entry1/SANS/name',outf,'name')

#-------- NXsource
outf.makegroup('source','NXsource')
outf.opengroup('source','NXsource')
copyData(inf,'/entry1/SANS/SINQ/name',outf,'name')
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
copyData(inf,'/entry1/SANS/Dornier-VS/lambda',outf,'wavelength')
data = numpy.array([0.1], numpy.float32)
outf.makedata('wavelength_spread','float32',[len(data)])
outf.opendata('wavelength_spread')
outf.putdata(data)
outf.closedata()
outf.closegroup() 

#----------- pre collimator slit
outf.makegroup('pre_collimator_slit','NXaperature')
outf.opengroup('pre_collimator_slit','NXaperature')
outf.makegroup('geometry','NXgeometry')
outf.opengroup('geometry','NXgeometry')
outf.makegroup('shape','NXshape')
outf.opengroup('shape','NXshape')
data = 'nxbox'
outf.makedata('shape','char',[len(data)])
outf.opendata('shape')
outf.putdata(data)
outf.closedata()
data = numpy.array([0.05, 0.05], numpy.float32)
outf.makedata('size','float32',[len(data)])
outf.opendata('size')
outf.putdata(data)
outf.closedata()

outf.closegroup()
outf.closegroup()
outf.closegroup()

#---------- collimator
outf.makegroup('collimator','NXcollimator')
outf.opengroup('collimator','NXcollimator')
outf.makegroup('geometry','NXgeometry')
outf.opengroup('geometry','NXgeometry')
outf.makegroup('shape','NXshape')
outf.opengroup('shape','NXshape')
data = 'nxcylinder'
outf.makedata('shape','char',[len(data)])
outf.opendata('shape')
outf.putdata(data)
outf.closedata()
copyData(inf,'/entry1/SANS/collimator/length',outf,'size')
outf.opendata('size')
outf.putattr('units','meter',dtype='char')
outf.closedata()
outf.closegroup()
outf.closegroup()
outf.closegroup()

#----------- pre sample slit
outf.makegroup('pre_sample_slit','NXaperature')
outf.opengroup('pre_sample_slit','NXaperature')
outf.makegroup('geometry','NXgeometry')
outf.opengroup('geometry','NXgeometry')
outf.makegroup('shape','NXshape')
outf.opengroup('shape','NXshape')
data = 'nxcylinder'
outf.makedata('shape','char',[len(data)])
outf.opendata('shape')
outf.putdata(data)
outf.closedata()
data = numpy.array([0.018], numpy.float32)
outf.makedata('size','float32',[len(data)])
outf.opendata('size')
outf.putdata(data)
outf.closedata()

outf.closegroup()
outf.closegroup()
outf.closegroup()


#---------- Detector
outf.makegroup('detector','NXdetector')
outf.opengroup('detector','NXdetector')
copyData(inf,'/entry1/SANS/detector/counts',outf,'data')
copyData(inf,'/entry1/SANS/detector/x_position',outf,'distance')
outf.opendata('data')
outf.putattr('signal',1,dtype='int32')
outf.closedata()
data = numpy.array([0.0075], numpy.float32)
outf.makedata('x_pixel_size','float32',[len(data)])
outf.opendata('x_pixel_size')
outf.putattr('units','meter',dtype='char')
outf.putdata(data)
outf.closedata()

data = numpy.array([0.0075], numpy.float32)
outf.makedata('y_pixel_size','float32',[len(data)])
outf.opendata('y_pixel_size')
outf.putattr('units','meter',dtype='char')
outf.putdata(data)
outf.closedata()

writeAngle(outf,'rotation_angle',0)
writeAngle(outf,'polar_angle',0)
writeAngle(outf,'azimuthal_angle',0)
writeAngle(outf,'aequatorial_angle',0)


outf.closegroup

outf.closegroup()
outf.closegroup()

#------------- NXdata
outf.makegroup('data','NXdata')
outf.opengroup('data','NXdata')
outf.closegroup()
outf.closegroup()
makeStink(outf,'/entry/instrument/detector/data','/entry/data')

inf.close()
outf.close()
print 'Done'
