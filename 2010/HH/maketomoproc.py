#!/usr/bin/python
#-------------------------------------------------------------
# A little program which generates an example tomography
# processed data file with purely invented data.
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
outf = nxs.open('nxtomoproc.hdf','w5')

#---------------- entry
outf.makegroup('entry','NXentry')
outf.opengroup('entry','NXentry')
makeTextData(outf,'title','Statue of Harry, 900 BH')
makeTextData(outf,'definition','NXtomoproc')
outf.opendata('definition')
data = 'http://svn.nexusformat.org/definitions/NXtomoproc.nxdl.xml'
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
outf.closegroup() # NXinstrument


#--------------- processing group
outf.makegroup('reconstruction','NXprocess')
outf.opengroup('reconstruction','NXprocess')
makeTextData(outf,'program','harry-construct')
makeTextData(outf,'version','3.0.7')
outf.makegroup('parameters','NXparameters')
outf.opengroup('parameters','NXparameters')
makeTextData(outf,'raw_file','nxtomo.hdf')
outf.closegroup()
outf.closegroup()

#------------------- sample group
outf.makegroup('sample','NXsample')
outf.opengroup('sample','NXsample')
makeTextData(outf,'name','Statue of Harry, 900 BH, Silver')
outf.closegroup()

#--------- data group
outf.makegroup('data','NXdata')
outf.opengroup('data','NXdata')
data = numpy.ones((256,256,256),numpy.dtype('int16'))
data.fill(77)
putArrayData(outf,'data',data)
outf.opendata('data')
outf.putattr('units','transparency',dtype='char')
outf.closedata()

data = numpy.ones((1),numpy.dtype('float32'))
data[0] = 0.0007
putArrayData(outf,'scale_factor',data)

data = numpy.arange(0.,256.)
putArrayData(outf,'x',data)
outf.opendata('x')
outf.putattr('units','mm',dtype='char')
outf.closedata()

putArrayData(outf,'y',data)
outf.opendata('y')
outf.putattr('units','mm',dtype='char')
outf.closedata()

putArrayData(outf,'z',data)
outf.opendata('z')
outf.putattr('units','mm',dtype='char')
outf.closedata()


outf.closegroup() # data

outf.closegroup() # entry


outf.close()
