

BIN=dhcp-client dhcp-client.exe dhcp-client.d 
LDLIBS = -lpcap




all:
	@echo "start compile"
	make -C ./c all
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -o dhcp-client. main.go 
	CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o dhcp-client.exe main.go 
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build  -o dhcp-client main.go

clean:
	rm -rf $(BIN)
	make -C ./c clean
