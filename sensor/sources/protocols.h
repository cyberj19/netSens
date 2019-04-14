#pragma once
#include <pcap.h>

#define ARP_REQUEST 1
#define ARP_REPLY 2

typedef struct {
    u_char dst[6];
    u_char src[6];
    u_char type[2];
} ether_header;

typedef struct {
	u_int16_t htype;
	u_int16_t ptype;
	u_char hlen;
	u_char plen;
	u_int16_t oper;
    u_char sha[6];
    u_char spa[4];
    u_char tha[6];
    u_char tpa[4];
} arp_packet;

int is_arp(const u_char *packet);
int is_dhcp(const u_char *packet);