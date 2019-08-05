#include <stdio.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
FILE *output;

int main(int argc, char **argv) {
	
	if (argc < 2) {
        printf("ERROR expected device name in command line argument\n");
        return 1;
	}
	char *iface = argv[1];
	if (argc == 3)
    {
        output = fopen(argv[2], "w+");
        //		printf("INFO capturing to file %s\n", argv[2]);
        if (output == NULL)
        {
            fprintf(stdout, "FATAL unable to open file");
			fflush(output);
			return 1;
        }
    }
    else
    {
        output = stdout;
    }
    fprintf(output, "INIT SIM %s\n", argv[1]);
    fflush(output);
	
	while (1) {
		fprintf(output, "PACKET eth:ethertype:arp,");
		time_t now = time(NULL);
		fprintf(output, "%ld,", now);
		fprintf(output, "12:13:14:15,");
		fprintf(output, "192.168.1.125,");
		fprintf(output, "192.168.1.126");
		fprintf(output, "\n");
		fflush(output);
		sleep(1);
	}
}

