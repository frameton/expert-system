from intro import display_42_logo
from home import *
import argparse
from get_gen_params import *
from save_params import *
import sys



if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-a", help="application format", action="store_true")
  parser.add_argument("-p", help="path file dataset  ->  expert-system.py -p [FILE_PATH]", type=str)
  args = parser.parse_args()

  if args.a:
    display_42_logo()
    home_step()
  
  elif args.p:
    params = get_gen_params()
    params["path"] = args.p
    params = expert_system_program(params)
    save_params(params)

  elif len(sys.argv) == 1:
    print("usage: expert-system.py [-h] [-a] [-p P]")
    print("       -h for more informations.")

  exit()