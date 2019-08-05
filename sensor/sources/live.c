#include <stdio.h>
#include "printers.h"
#include "protocols.h"
#include <pcap.h>
#include <time.h>
#include <string.h>
#include <netinet/in.h>
#include <netinet/if_ether.h>
#include <net/ethernet.h>

pcap_t *handle;
FILE *output;

void packet_handler(u_char *args, const struct pcap_pkthdr *header, const u_char *packet);

int main(int argc, char **argv)
{
    char error_buffer[PCAP_ERRBUF_SIZE];
    bpf_u_int32 netaddr = 0, mask = 0;
    struct bpf_program filter;
    int snapshot_len = 1028;
    int promiscuous = 0;
    int timeout = 1000;
    if (argc < 2)
    {
        printf("ERROR expected device name in command line argument\n");
        return 1;
    }

    if (argc == 3)
    {
        output = fopen(argv[2], "w+");
        //		printf("INFO capturing to file %s\n", argv[2]);
        if (output == NULL)
        {
            fprintf(stdout, "FATAL unable to open file");
        }
    }
    else
    {
        output = stdout;
    }
    fprintf(output, "INIT LIVE %s\n", argv[1]);
    fflush(output);
    handle = pcap_open_live(argv[1], snapshot_len, promiscuous, timeout, error_buffer);
    if (handle == NULL)
    {
        fprintf(output, "ERROR %s\n", error_buffer);
        return 1;
    }

    if (pcap_lookupnet(argv[1], &netaddr, &mask, error_buffer) == -1)
    {
        fprintf(output, "ERROR %s\n", error_buffer);
        return 1;
    }

    if (pcap_compile(handle, &filter, "arp or port 68 or port 67", 1, mask) == -1)
    {
        fprintf(output, "ERROR %s\n", pcap_geterr(handle));
        return 1;
    }

    if (pcap_setfilter(handle, &filter) == -1)
    {
        fprintf(output, "ERROR %s\n", pcap_geterr(handle));
        return 1;
    }

    pcap_loop(handle, 0, packet_handler, NULL);
    return 0;
}

void packet_handler(u_char *args, 
                    const struct pcap_pkthdr *header, 
                    const u_char *packet)
{
    if (is_arp(packet)) {
        print_arp(output, header, packet);
    } else {
        print_dhcp(output, header, packet);
    }
}