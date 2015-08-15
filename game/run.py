#!/usr/bin/env python
import sys, os, inspect
top_path = os.path.dirname(os.path.dirname(os.path.join(os.getcwd() ,inspect.getfile(inspect.currentframe()))))
deps_path = os.path.join(top_path, "deps")
image_path = os.path.join(top_path, "images")
sound_path = os.path.join(top_path, "sounds")
model_path = os.path.join(top_path, "models")
sys.path = [top_path, deps_path, image_path, sound_path, model_path] + sys.path
import argparse
import game
import signal
from game.model import managers

# manager initialization

def run_server(args):
    managers.Server(port=args.port, run_local=args.local)

def run_client(args):
    managers.Client(remote_address=args.remote_address,
                    remote_port=args.remote_port,
                    local_port=args.local_port,
                    run_local=args.local)

# top-level parser
parser = argparse.ArgumentParser(description="Run the game server or client.")
subparsers = parser.add_subparsers(title="required arguments")

# parser for the "server" command
parser_s = subparsers.add_parser("server",
                                 help="run game server",
                                 description="Run game server.")
parser_s.add_argument("-p", "--port",
                      default=8000, type=int,
                      help="port to listen on (default: %(default)s)")
parser_s.add_argument("-L", "--local", action='store_true',
                      help="Run as a local server (default: %(default)s)")
parser_s.set_defaults(func=run_server)

# parser for the "client" command
parser_c = subparsers.add_parser("client",
                                 help="run game client",
                                 description="Run game client.")
parser_c.add_argument("-a", "--remote_address",
                      metavar="ADDRESS", default="127.0.0.1",
                      help="server address to connect to (default: %(default)s)")
parser_c.add_argument("-p", "--remote_port",
                      metavar="PORT", default=8000, type=int,
                      help="server port to connect to (default: %(default)s)")
parser_c.add_argument("-l", "--local_port",
                      metavar="PORT", default=9000, type=int,
                      help="local port to listen on (default: %(default)s)")
parser_c.add_argument("-L", "--local", action='store_true',
                        help="Run as a local server (default: %(default)s)")

parser_c.set_defaults(func=run_client)

# get args, initialize appropriate manager
args = parser.parse_args()
args.func(args)

# cleanup on ^C input (doesn't work on windows)
def signal_handler(signal, frame):
    print "\nExiting..."
    game.manager.cleanup()
    sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)
# signal.pause()