# Detect operating system in Makefile.
# Author: He Tao
# Date: 2015-05-30

osflag 				:=
ifeq ($(os),windows_nt)
	osflag += win32
else
	uname_s := $(shell uname -s)
	ifeq ($(uname_s),linux)
		osflag += linux
	endif
endif

all:
	ifeq($(OSFLAG),win32)
		@echo $(OSFLAG)
	else
		@echo "LiNuX"
	endif
