#pragma once
#include "queuePrinter.h"
#include <pcap.h>
#include <string.h>

const int snapshot_len = 1028;
const int promiscuous = 0;
const int timeout = 1000;
    
typedef struct {
    std::string protocol;
    std::string interface;
} ListenerSpec;

class Listener {
    pcap_t* handle;
    QueuePrinter* printer;
    ListenerSpec spec;
    std::ostringstream stringStream;

    public:
        Listener(ListenerSpec spec, QueuePrinter* printer);
    private:
        void operator <<(const char *str);
}