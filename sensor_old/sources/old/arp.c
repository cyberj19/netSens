#include <stdio.h>
#include <signal.h>
#include <pcap.h>
#include <time.h>
#include <string.h>
#include <netinet/in.h>
#include <netinet/if_ether.h>
#include <net/ethernet.h>

#define ARP_REQUEST 1
#define ARP_REPLY 2
typedef struct marphdr {
	u_int16_t htype;
	u_int16_t ptype;
	u_char hlen;
	u_char plen;
	u_int16_t oper;
	u_char sha[6];
	u_char spa[4];
	u_char tha[6];
	u_char tpa[4];
} marphdr_t;

pcap_t *handle;
FILE *output;
volatile sig_atomic_t done = 0;

void my_packet_handler(u_char *args, const struct pcap_pkthdr *header, const u_char *packet);
/*
void term(int signum) {
	fprintf(output,"TERMINATE\n");
	done = 1;
	pcap_breakloop(handle);
}
*/

int main(int argc, char **argv) {
	struct sigaction action;
	char error_buffer[PCAP_ERRBUF_SIZE];
	bpf_u_int32 netaddr=0, mask=0;
	struct bpf_program filter;
	int snapshot_len = 1028;
	int promiscuous = 0;
	int timeout = 1000;

/*
	memset(&action, 0, sizeof(action));
	action.sa_handler = term;
	sigaction(SIGTERM, &action, NULL);
	sigaction(SIGKILL, &action, NULL);
*/
//	setbuf(stdout, NULL);
	if (argc < 2 ) {
		printf("ERROR expected device name in command line argument\n");
		return 1;
	}
	
	if (argc == 3) {
		output = fopen(argv[2], "w+");
//		printf("INFO capturing to file %s\n", argv[2]);
		if (output == NULL) {
			fprintf(stdout, "FATAL unable to open file");
		}
	} else {
		output = stdout;
	}
	fprintf(output,"INIT %s\n", argv[1]);
	fflush(output);
	handle = pcap_open_live(argv[1],snapshot_len,promiscuous,timeout,error_buffer);
	if (handle == NULL) {
		fprintf(output, "ERROR %s\n", error_buffer);
		return 1;
	}
	
	if (pcap_lookupnet(argv[1],&netaddr,&mask,error_buffer) == -1) {
		fprintf(output, "ERROR %s\n",error_buffer);
		return 1;
	}
	
	if (pcap_compile(handle,&filter,"arp",1,mask)==-1) {
		fprintf(output, "ERROR %s\n",pcap_geterr(handle));
		return 1;
	}
	
	if (pcap_setfilter(handle,&filter) == -1) {
		fprintf(output, "ERROR %s\n", pcap_geterr(handle));
		return 1;
	}
	
	pcap_loop(handle, 0, my_packet_handler, NULL);
	return 0;
}

void print_mac_addr(FILE* file, u_char *addr) {
	int i;
	for (i = 0; i < 5; i++) fprintf(file, "%02X:", addr[i]);
	fprintf(file,"%02X",addr[i]);
}

void print_ip_addr(FILE* file, u_char *addr) {
	int i;
	for (i = 0; i < 3; i++) fprintf(file, "%d.", addr[i]);
	fprintf(file,"%d",addr[i]);
}
void my_packet_handler(u_char *args, const struct pcap_pkthdr *header, const u_char *packet) {
	int i;
	marphdr_t* arpheader = (struct marphdr*)(packet+14);
	
	//printf("\n\nReceived Packet Size: %d bytes\n", header->len);
	//printf("Hardware type: %s\n", (ntohs(arpheader->htype) == 1) ? "Ethernet" : "Unknown"); 
	//printf("Protocol type: %s\n", (ntohs(arpheader->ptype) == 0x0800) ? "IPv4" : "Unknown"); 
	//printf("Operation: %s\n", (ntohs(arpheader->oper) == ARP_REQUEST)? "ARP Request" : "ARP Reply"); 

	// protocol, timestamp, source_mac, source_ip, target_ip
	if (arpheader->oper == ARP_REPLY) {
		fprintf(output, "DEBUG dropped ARP reply packet\n");
		return;
	}
	fprintf(output, "PACKET eth:ethertype:arp,");
	fprintf(output, "%d.%06d,",(int)header->ts.tv_sec, (int)header->ts.tv_usec);
	
	print_mac_addr(output, arpheader->sha);
	fprintf(output,",");
	
	print_ip_addr(output, arpheader->spa);
	fprintf(output,",");
	
	print_ip_addr(output, arpheader->tpa);
		
	fprintf(output, "\n");
	
	fflush(output);

/*
	if (done) {
		pcap_breakloop(handle);
	}
*/
}