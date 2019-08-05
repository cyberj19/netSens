all: linux2_live linux2_playback

linux2_live: printers.c protocols.c live.c printers.h protocols.h
	gcc printers.c protocols.c live.c -lpcap -o linux2_live
	mv linux2_live ../binaries/
	
linux2_playback: printers.c protocols.c playback.c printers.h protocols.h
	gcc printers.c protocols.c playback.c -lpcap -o linux2_playback
	mv linux2_playback ../binaries/