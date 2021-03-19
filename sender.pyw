#    Copyright (C) 2021 Konrad Sekuła
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# sender.pyw

class Sender():
    def Send(_host, _port, _request, __ssl):
        import socket
        data=""
        host = _host
        port = _port
        if not __ssl:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((host, port))
            s.sendall(_request.encode())
            data = s.recv(8192)
            s.close()
        else:
            import ssl
            ssl_context=ssl.create_default_context()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ws=ssl.wrap_socket(s,ssl_version=ssl.PROTOCOL_SSLv23,ciphers="AES256-SHA")
            ws.settimeout(10)
            ws.connect((host, port))
            ws.sendall(_request.encode())
            data = ws.recv(8192)
            ws.close()

        return data