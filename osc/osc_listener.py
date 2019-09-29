"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math

import datetime
import atexit
import signal
import pprint



from pythonosc import dispatcher
from pythonosc import osc_server




def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass


all_logs = {}

def log_message(address, message):
    my_time = datetime.datetime.now()
    my_log = "{} - Address: {}, Message: {}".format(my_time ,address, message)
    #print(my_log)
    
    log_queue = all_logs.get(address)
    if log_queue is None:
        new_log = []
        new_log.append(my_log)
        all_logs[address] = new_log
    else:
        log_queue.append(my_log)
        
    pprint.pprint(all_logs)
      
@atexit.register
def print_data_info():
    print("Program terminated!")

#atexit.register(print_data_info)
signal.signal(signal.SIGTERM, print_data_info)
signal.signal(signal.SIGINT, print_data_info)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="192.168.0.50", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5010, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  #dispatcher.set_default_handler(print, needs_reply_address=True)
  dispatcher.set_default_handler(log_message, needs_reply_address=False)
  #dispatcher.map("/filter", print)
  #dispatcher.map("/volume", print_volume_handler, "Volume")
  #dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
  #dispatcher.map("/iPhone/x", print)
  #dispatcher.map("/iPhone/y", print)
  #dispatcher.map("/iPhone/z", print)
  #dispatcher.map("/iPhone/*", print)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  #server = osc_server.BlockingOSCUDPServer(
  #    (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
