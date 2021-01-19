# https://pypi.org/project/pyftpdlib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

class FtpServerSample:
    @staticmethod
    def start():
        os.makedirs(r"c:\data\ftpserver", exist_ok=True)
        with open(r"c:\data\ftpserver\test.txt", "w") as fl:
            fl.write('test')

        authorizer = DummyAuthorizer()
        authorizer.add_user("user", "12345", r"c:\data\ftpserver", perm="elradfmwMT")
        # authorizer.add_anonymous("/home/nobody")

        handler = FTPHandler
        handler.authorizer = authorizer

        server = FTPServer(("127.0.0.1", 21), handler)
        server.serve_forever()

def main():
    FtpServerSample.start()


if __name__ == '__main__':
    main()
