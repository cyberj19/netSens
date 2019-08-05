all: linux2_listener

linux2_listener: printers.c protocols.c listener.c printers.h protocols.h
	gcc printers.c protocols.c listener.c -lpcap -o linux2_listener
	mv linux2_listener ../binaries/

