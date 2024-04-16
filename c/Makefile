
BIN=DHCPclient DHCPserver dhcp-client
LDLIBS = -lpcap

all: $(BIN)
	echo "Build complete"

DHCPclient: DHCPclient.c
	gcc -o DHCPclient DHCPclient.c

DHCPserver: DHCPserver.c
	gcc -o DHCPserver DHCPserver.c

#apt-get install libpcap-dev
dhcp-client: dhcp-client.c 


info:
	echo "This is a DHCP client program"
	echo "$(BIN) is the output file"
clean:
	rm -f $(BIN)