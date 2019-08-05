#include "protocols.h"

int is_arp(const u_char *packet) {
    ether_header* ether = (ether_header*)packet;
    if (ether->type[0] == 0x08 && 
        ether->type[1] == 0x06)
        return 1;
    return 0;
}