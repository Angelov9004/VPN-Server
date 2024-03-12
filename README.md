Connect to different IP addresses with your VPN server, you would typically modify your VPN server configuration to listen on multiple IP addresses or interface addresses.
Then, clients can connect to these different IP addresses to establish VPN connections.

The VPNServer class now accepts a list of (host, port) tuples in its constructor, allowing you to specify multiple IP addresses and ports for the VPN server to listen on.
The start_servers method starts servers on all specified IP addresses and ports asynchronously.
The VPNApp class is modified to create a VPNServer instance with multiple IP addresses and ports.
You can specify as many (host, port) tuples as needed in the VPNServer constructor to listen on multiple IP addresses and ports.
