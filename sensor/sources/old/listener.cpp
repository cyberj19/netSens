#include "listener.h"

using namespace std;

Listener::Listener(ListenerSpec spec, QueuePrinter* printer) {

    this->printer = printer;
    this->spec = spec;

    char error_buffer[PCAP_ERRBUF_SIZE];
    
    handle = pcap_open_live(spec.interface, snapshot_len, promiscuous, timeout, error_buffer);

    if (handle == NULL)
    {
        ostringstream ss;
        ss << "ERROR unable to load listener " << error_buffer << endl;
        printer->print(ss.str())
        return;
    }

    
    if (pcap_lookupnet(spec.interface, &netaddr, &mask, error_buffer) == -1)
    {
        ostringstream ss;
        ss << "ERROR unable to load listener " << error_buffer << endl;
        printer->print(ss.str());
        return;
    }

    std::string filter_string;
    if (strcmp(spec.interface.c_str(), "arp")) {
        filter_string = std::string("arp");
    } else {
        filter_string = std::string("port 68");
    }
    if (pcap_compile(handle, &filter, filter_string.c_str(), 1, mask) == -1)
    {
        ostringstream ss;
        ss << "ERROR unable to compile filter: " << pcap_geterr(handle) << endl;
        return;
    }
}

void Listener::operator<<(const char* str) {
    stringStream << str;

    if (strcmp(str,"\n")) {
        printer->print(stringStream.str());
        stringStream = ostreamstring();
    }

    return this;
}