#!/usr/bin/python
#-------------------------------------------------------------
# A little program which generates an example XAS raw data
# file with purely invented data.
#
# copyright: Do not even consider to bother me
#
# Mark Koennecke, October 2010
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
outf = nxs.open('nxxasraw.hdf','w5')

#---------------- entry
outf.makegroup('entry','NXentry')
outf.opengroup('entry','NXentry')
makeTextData(outf,'title','CucumberOxid')
makeTextData(outf,'start_time','2010-07-30 07:07:07')
makeTextData(outf,'definition','NXxas')
outf.opendata('definition')
data = 'http://svn.nexusformat.org/definitions/NXxas.nxdl.xml'
outf.putattr('URL',data)
outf.closedata()

#----------------- instrument
outf.makegroup('instrument','NXinstrument')
outf.opengroup('instrument','NXinstrument')
makeTextData(outf,'name','S-XAS')

#---------------- source
outf.makegroup('source','NXsource')
outf.opengroup('source','NXsource')
makeTextData(outf,'name','IINS')
makeTextData(outf,'probe','x-ray')
makeTextData(outf,'type','synchrotron source')
outf.closegroup() 

#---------------- monochromator
outf.makegroup('monochromator','NXmonochromator')
outf.opengroup('monochromator','NXmonochromator')
data = numpy.ones((1024),numpy.dtype('float32'))
data.fill(.78)
putArrayData(outf,'wavelength',data)
outf.closegroup() 


#----------- incoming_beam
outf.makegroup('incoming_beam','NXdetector')
outf.opengroup('incoming_beam','NXdetector')
data = numpy.ones((1024),numpy.dtype('int32'))
data.fill(1000)
putArrayData(outf,'data',data)
outf.closegroup() 

#----------- absorbed_beam
outf.makegroup('absorbed_beam','NXdetector')
outf.opengroup('absorbed_beam','NXdetector')
data = numpy.ones((1024),numpy.dtype('int32'))
data.fill(500)
putArrayData(outf,'data',data)
outf.opendata('data')
data = 'wavelength'
outf.putattr('axes',data)
data = 1
outf.putattr('signal',data)
outf.closedata()
outf.closegroup() 

outf.closegroup() # NXinstrument

#------------------- sample group
outf.makegroup('sample','NXsample')
outf.opengroup('sample','NXsample')
makeTextData(outf,'name','CucumberOxid')
outf.closegroup()

#------------------ monitor
outf.makegroup('control','NXmonitor')
outf.opengroup('control','NXmonitor')
data = numpy.ones((1024),numpy.dtype('int32'))
data.fill(10000)
putArrayData(outf,'data',data)
data = numpy.ones((1),numpy.dtype('int32'))
data.fill(10000)
putArrayData(outf,'preset',data)
makeTextData(outf,'mode','monitor')

outf.closegroup()



#--------- data group
outf.makegroup('data','NXdata')
outf.opengroup('data','NXdata')
outf.closegroup() # data
outf.closegroup() # entry

makeStink(outf,'/entry/instrument/absorbed_beam/data','/entry/data')
makeStink(outf,'/entry/instrument/monochromator/wavelength','/entry/data')


outf.close()
