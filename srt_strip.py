import re
import sys
import argparse
from collections import namedtuple

SrtEntry = namedtuple("SrtEntry", ("frame", "time_range", "data", "padding"))

parser = argparse.ArgumentParser()
parser.add_argument('-i', "--in_file", metavar='I', required=True, type=open, help='Input .srt file to read from')
parser.add_argument('-o', "--out_file", metavar='O', required=True, type=argparse.FileType('w'), help='Output .srt file to write to')
group = parser.add_mutually_exclusive_group()
group.add_argument('-k', "--keep_vars", action='append', default=[], help='Variables to keep, cannot be used with drop_vars or interactive')
group.add_argument('-d', "--drop_vars", action='append', default=[], help='Variables to drop, cannot be used with keep_vars or interactive')
parser.add_argument("--interactive", help='Interactive Mode', action='store_true')

args = parser.parse_args()

keep_vars = set(args.keep_vars) if args.keep_vars is not None else set()
drop_vars = args.drop_vars if args.drop_vars is not None else []

def read_message_frame(f):
    try:
        return SrtEntry(
            next(f).strip(),
            next(f).strip(),
            {k: v for k, v in map(lambda x: x.split(':'), next(f).strip().split(' '))},
            next(f).strip())
    except StopIteration:
        return None


with args.in_file as f:
    if args.interactive is not None:
        data_args = read_message_frame(f)
        toggleable_variables = tuple(data_args.data.keys())
        keep_vars = set(toggleable_variables) if len(keep_vars) == 0 else keep_vars
        for var in drop_vars:
            keep_vars.discard(var)
        f.seek(0)
        while True:
            print("I would like to output...")
            for i, arg in enumerate(toggleable_variables):
                print(f'{i+1:2d}: [{"█" if arg in keep_vars else " "}] {arg:12s}', end='\n' if i%3==2 or i+1 == len(toggleable_variables) else '')
            print(f'{len(toggleable_variables) + 1:2d}: Toggle All')
            print(f'{len(toggleable_variables) + 2:2d}: Done')
            print("Select a variable to toggle")
            toggle_var = input()
            try:
                    selection = int(toggle_var)
                    if selection-1 in range(len(toggleable_variables)):
                        toggle_var = toggleable_variables[selection - 1]
                    elif selection == len(toggleable_variables)+1:
                        keep_vars = set(toggleable_variables).difference(keep_vars)
                    elif selection == len(toggleable_variables)+2:
                        break
            except ValueError:
                pass
            if toggle_var in data_args.data:
                if toggle_var in keep_vars:
                    keep_vars.remove(toggle_var)
                else:
                    keep_vars.add(toggle_var)
            else:
                print("Invalid input")

    with args.out_file as f_out:
        while True:
            work_data = read_message_frame(f)
            if work_data:
                for arg in drop_vars:
                    del work_data.data[arg]
                for arg in list(work_data.data.keys()):
                    if arg not in keep_vars:
                        del work_data.data[arg]
                f_out.write(f"{work_data.frame}\n")
                f_out.write(f"{work_data.time_range}\n")
                f_out.write(f"{' '.join([f'{k}:{v}' for k, v in work_data.data.items()])}\n")
                f_out.write(f"{work_data.padding}\n")
            else:
                break