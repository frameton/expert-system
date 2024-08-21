from app_format_src.intro import display_42_logo
from app_format_src.home import home_step
from app_format_src.get_gen_params import get_gen_params
from app_format_src.save_params import save_params
from expert_system_program import expert_system_program
from tester import tester_mode
import argparse
import sys



if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-a", help="application format", action="store_true")
  parser.add_argument("-p", help="path file dataset  ->  expert-system.py -p [FILE_PATH]", type=str)
  parser.add_argument("-t", help="tester mode", action="store_true")
  args = parser.parse_args()

  if args.a:
    display_42_logo()
    home_step()
  
  elif args.p:
    params = get_gen_params()
    params["path"] = args.p
    params = expert_system_program(params)
    save_params(params)
  
  elif args.t:
    tester_mode()
    

  elif len(sys.argv) == 1:
    print("usage: expert-system.py [-h] [-a] [-p P] [-t]")
    print("       -h for more informations.")

  exit()