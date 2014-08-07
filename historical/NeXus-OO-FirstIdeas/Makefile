#--------------------------------------------------------------------------
# Makefile for making slides with the prosper latex package
# The result will be a pdf file which can be displayed with
#
# xpdf -fullscreen filename
#
# Before this can work, setenv TEXINPUTS .:/data/koenneck/lib/prosper:
# must be issued on the command prompt
#
# Mark Koennecke, October 2003
#-------------------------------------------------------------------------
.SUFFIXES:
.SUFFIXES: .tex .pdf

SOURCE=NeXusOBJ

.tex.pdf:
	latex $*.tex
	dvips  -T 24cm,30cm  -Ppdf -o $*.ps $*.dvi
	ps2pdf -dPDFsettings=/prepress $*.ps $*.pdf

all: NeXusOBJ.pdf 


clean:
	- rm napi.ps
	- rm napi.pdf
	- rm *.dvi
	- rm *.aux
	- rm *.log

print:	$(SOURCE).tex
	latex $(SOURCE).tex
	dvips -t a4 -o $(SOURCE).ps $(SOURCE)
	
	