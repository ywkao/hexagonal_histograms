CC       := g++ # This is the main compiler
BUILDDIR := build
INC 	 := -I include
CFLAGS   := $(shell root-config --cflags) -fPIC -g -O3 -Wall -Wextra #-Wno-write-strings -D_FILE_OFFSET_BITS=64 -DDROP_CGAL
ROOTLIBS := $(shell root-config --libs) -lMinuit -lMLP -lXMLIO -lTMVA -lGenVector

TARGET   := build/libHGCalCell.so

all: ${TARGET}

build/libHGCalCell.so: build/HGCalCell.o
	@mkdir -p $(BUILDDIR)
	$(CC) $(CFLAGS) $(INC) -shared -o $@ $^
	@echo "$(TARGET) is built"

build/HGCalCell.o: src/HGCalCell.cc include/HGCalCell.h
	@mkdir -p $(BUILDDIR)
	$(CC) $(CFLAGS) $(INC) -c -o $@ $<

.PHONY: clean
clean:
	/bin/rm -r $(BUILDDIR)
