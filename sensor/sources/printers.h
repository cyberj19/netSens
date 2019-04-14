#pragma once
#include <stdio.h>
#include <pcap.h>


void print_dhcp(FILE* file, const struct pcap_pkthdr *, const u_char *);
void print_arp(FILE* file, const struct pcap_pkthdr *, const u_char *);
void print_ip_addr(FILE *file, const u_char *addr);
void print_mac_addr(FILE *file, const u_char *addr);