# There is a problem with this makefile
# It does not process nxh5write properly
.SUFFIXES:
.SUFFIXES: .c .o

.c.o:
	$(CC) -g -c $*.c

#all: nxh5write nxh5read

nx5hwrite: nxh5write.o
	$(CC) -o nxh5write nxh5write.o -lhdf5 -lz -lm

nxh5read: nxh5read.o
	$(CC) -o nxh5read nxh5read.o -lhdf5 -lz -lm


clean: 
	- rm nxh5write nxh5read
	- rm *.o


