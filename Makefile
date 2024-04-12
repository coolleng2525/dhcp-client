

BIN=dhcp-client dhcp-client.exe dhcp-client.d

 -o dhcp-client.exe -o dhcp-client.exe -o dhcp-client.exe -o dhcp-client.exe
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d -o dhcp-client.exe
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d -o dhcp-client.exe
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d -o dhcp-client.exe
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d -o dhcp-client.exe
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d -o dhcp-client.exe
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build main.go -o dhcp-client.d

all:
	@echo "start compile"
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -o dhcp-client.d main.go 
	CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o dhcp-client.exe main.go 
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build  -o dhcp-client main.go

clean:
	rm -rf $(BIN)
