#!/usr/bin/python
#-------------------------------------------------------------
# A little program which generates an example tomography raw data
# file with purely invented data.
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

def makeTextData(outf, name, value):
    outf.makedata(name,'char',[len(value)])
    outf.opendata(name)
    outf.putdata(value)
    outf.closedata()


def putArrayData(outf,name, ardata):
    outf.makedata(name,ardata.dtype.name,ardata.shape)
    outf.opendata(name)
    outf.putdata(ardata)
    outf.closedata()

def makeStink(outf, targetpath, topath):
    outf.openpath(targetpath)
    id = outf.getdataID()
    outf.openpath(topath)
    outf.makelink(id)

#------------------- open file
outf = nxs.open('nxtomo.hdf','w5')

#---------------- entry
outf.makegroup('entry','NXentry')
outf.opengroup('entry','NXentry')
makeTextData(outf,'title','Statue of Harry, 900 BH')
makeTextData(outf,'start_time','2005-07-30 07:07:07')
makeTextData(outf,'end_time','2005-08-02 22:07:22')
makeTextData(outf,'definition','NXtomo')
outf.opendata('definition')
data = 'http://svn.nexusformat.org/definitions/NXtomo.nxdl.xml'
outf.putattr('URL',data)
outf.closedata()

#----------------- instrument
outf.makegroup('instrument','NXinstrument')
outf.opengroup('instrument','NXinstrument')
makeTextData(outf,'name','ICON @ SINQ')

#---------------- source
outf.makegroup('source','NXsource')
outf.opengroup('source','NXsource')
makeTextData(outf,'name','SINQ')
makeTextData(outf,'probe','neutron')
makeTextData(outf,'type','spallation neutron source')
outf.closegroup() 

#----------- brightfield
outf.makegroup('bright_field','NXdetector')
outf.opengroup('bright_field','NXdetector')
data = numpy.ones((2,1024,1024),numpy.dtype('int16'))
data.fill(1000)
putArrayData(outf,'data',data)
data = numpy.ones(2,numpy.dtype('int32'))
data[1] = 95
putArrayData(outf,'sequence_number',data)
outf.closegroup() 

#----------- darkfield
outf.makegroup('dark_field','NXdetector')
outf.opengroup('dark_field','NXdetector')
data = numpy.ones((2,1024,1024),numpy.dtype('int16'))
putArrayData(outf,'data',data)
data = numpy.ones(2,numpy.dtype('int32'))
data[0] = 2
data[1] = 94
putArrayData(outf,'sequence_number',data)
outf.closegroup() 

#----------- sample images
outf.makegroup('sample','NXdetector')
outf.opengroup('sample','NXdetector')
data = numpy.ones((90,1024,1024),numpy.dtype('int16'))
data.fill(77)
putArrayData(outf,'data',data)
data = numpy.arange(3,93)
putArrayData(outf,'sequence_number',data)
data = numpy.ones((1),numpy.dtype('float32'))
data[0] = 0.023
putArrayData(outf,'x_pixel_size',data)
outf.opendata('x_pixel_size')
outf.putattr('units','meter',dtype='char')
outf.closedata()
putArrayData(outf,'y_pixel_size',data)
outf.opendata('y_pixel_size')
outf.putattr('units','meter',dtype='char')
outf.closedata()
data[0] = 0.60
putArrayData(outf,'distance',data)
outf.opendata('distance')
outf.putattr('units','meter',dtype='char')
outf.closedata()

outf.closegroup() 



outf.closegroup() # NXinstrument

#------------------- sample group
outf.makegroup('sample','NXsample')
outf.opengroup('sample','NXsample')
makeTextData(outf,'name','Statue of Harry, 900 BH, Silver')
data = numpy.arange(0.,90.)
putArrayData(outf,'rotation_angle',data)
outf.opendata('rotation_angle')
outf.putattr('units','degree',dtype='char')
outf.closedata()
outf.closegroup()

#------------------ monitor
outf.makegroup('control','NXmonitor')
outf.opengroup('control','NXmonitor')
data = numpy.ones((94),numpy.dtype('int32'))
data.fill(10000)
putArrayData(outf,'integral',data)
outf.closegroup()


#------------------ user group
outf.makegroup('user','NXuser')
outf.opengroup('user','NXuser')

makeTextData(outf,'name','Harry User')
makeTextData(outf,'address','44, Harry Close, Harriston, HX27O5, United Harrydom')
makeTextData(outf,'owner_email','harry.user@harry.co.uh')
makeTextData(outf,'owner_telephone_number','0077-312-556612398')
makeTextData(outf,'owner_fax_number','0077-312-556612887')

outf.closegroup()


#--------- data group
outf.makegroup('data','NXdata')
outf.opengroup('data','NXdata')
outf.closegroup() # data
outf.closegroup() # entry

makeStink(outf,'/entry/instrument/sample/data','/entry/data')
makeStink(outf,'/entry/sample/rotation_angle','/entry/data')


outf.close()
