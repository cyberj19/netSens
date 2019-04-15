#include "printers.h"
#include "protocols.h"

void print_mac_addr(FILE *file, 
                    const u_char *addr)
{
    int i;
    for (i = 0; i < 5; i++)
        fprintf(file, "%02X:", addr[i]);
    fprintf(file, "%02X", addr[i]);
}

void print_ip_addr(FILE *file, 
                    const u_char *addr)
{
    int i;
    for (i = 0; i < 3; i++)
        fprintf(file, "%d.", addr[i]);
    fprintf(file, "%d", addr[i]);
}
void print_dhcp(FILE *file, 
                const struct pcap_pkthdr *header, 
                const u_char *packet)
{
    fprintf(file,"PACKET eth:ethertype:ip:udp:bootp,");
	fprintf(file, "%d.%06d,",(int)header->ts.tv_sec, (int)header->ts.tv_usec);
	print_mac_addr(file,packet+6);
	print_param_req_list(file,packet+DHCP_OPTIONS);
    fprintf(file, "\n");
    fflush(file);
}

void print_param_req_list(FILE *file,
                           const u_char *packet)
{
	int i=0;
	int option=(int)packet[i];
	int op_len=(int)packet[i+1];
	while(option != 55 && op_len != 0){
		i+=op_len+2;
		option=(int)packet[i];
        	op_len=(int)packet[i+1];
	}
	fprintf(file,",");
	if(option == 55){
		for(int j=i+2; j<op_len+i+1; j++){
			fprintf(file,"%d;",packet[j]);
		}
		fprintf(file,"%d",packet[op_len+i+1]);
	}
	else{
		fprintf(file,",");
	}

}
void print_arp(FILE* file,
                const struct pcap_pkthdr *header, 
                const u_char *packet)
{
    int i;
    arp_packet *arpheader = (arp_packet*)(packet + 14);
    if (arpheader->oper == ARP_REPLY)
    {
        fprintf(file, "DEBUG dropped ARP reply packet\n");
        return;
    }
    fprintf(file, "PACKET eth:ethertype:arp,");
    fprintf(file, "%d.%06d,", (int)header->ts.tv_sec, (int)header->ts.tv_usec);

    print_mac_addr(file, arpheader->sha);
    fprintf(file, ",");

    print_ip_addr(file, arpheader->spa);
    fprintf(file, ",");

    print_ip_addr(file, arpheader->tpa);

    fprintf(file, "\n");

    fflush(file);
}
