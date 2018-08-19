# openvpn-routing-wrapper

OpenVPN has introduced quite a serious bug which causes the routing commands to file - ruining your connection. Until a fix comes out, this tool takes care of manually re-executing the `ip route` commands for you.

## Usage

Pipe the output of OpenVPN to this wrapper.

    sudo openvpn company.conf | sudo openvpn-routing-wrapper.py



