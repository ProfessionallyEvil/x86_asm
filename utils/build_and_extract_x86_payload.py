#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program: build_and_extract_x86_payload.py

Date: 07/07/2021

Author: Travis Phillips

Purpose: This script will build a GAS source file object and extract
         its .text section and print it out as a formatted payload to
         be copied and pasted in other code.
"""
#######################################
#              Imports
#######################################
import sys
import os
import argparse
import tempfile
import subprocess
from shutil import copy

#######################################
#       Application Constants
#######################################
TITLE = "Build & Extract Payload"
VERSION = "v1.0"

#######################################
#       Color Constants
#######################################
RED = "\033[31;1m"
GRN = "\033[32;1m"
YEL = "\033[33;1m"
BLU = "\033[34;1m"
NON = "\033[0m"

########################################################################
#                         PRINTER FUNCTIONS
########################################################################
def print_info(msg: str, end: str="\n"):
    """ Print an info message. """
    print(f" [{BLU}*{NON}] {msg}", end=end)

def print_success(msg: str, end: str="\n"):
    """ Print a success message. """
    print(f" [{GRN}+{NON}] {msg}", end=end)

def print_error(msg: str, end: str="\n"):
    """ Print a failure message. """
    print(f" [{RED}-{NON}] \033[31;1mERROR:{NON} {msg}", end=end)

def print_key_val(key: str, val: str, end: str="\n"):
    """ Print a failure message. """
    print(f"{YEL}{key.rjust(23)}:{NON} {val}", end=end)

def format_bool(val: bool) -> str:
    """ Format bools for metadata output """
    if val:
        return f"{RED}TRUE{NON}"
    return f"{GRN}FALSE{NON}"

def print_c_payload(payload: bytes, buf: str, args: argparse.Namespace):
    """ Formats the payload output for C code. """
    fmt = "/////////////////////////////////////////////////////\n"
    fmt += f"//  source file: {os.path.basename(args.src_file)}\n"
    fmt += f"// payload size: {len(payload)}\n"
    fmt += "/////////////////////////////////////////////////////\n\n"
    fmt += "char payload[] = "
    i = 0
    padding = ""
    while i < len(buf):
        if i > 0:
            padding = "                 "
        if len(buf) - i >= 64:
            fmt += f"{padding}\"{buf[i:i+64]}\"\n"
        else:
            fmt += f"{padding}\"{buf[i:]}\"\n"
        i += 64
    fmt = f"{fmt[:-1]};\n"
    print(fmt)

def print_python_payload(payload: bytes, buf: str, args: argparse.Namespace):
    """ Formats the payload output for python code. """
    fmt = "#################################################\n"
    fmt += f"#  source file: {os.path.basename(args.src_file)}\n"
    fmt += f"# payload size: {len(payload)}\n"
    fmt += "#################################################\n\n"
    i = 0
    while i < len(buf):
        if i == 0:
            fmt += "payload  = "
        else:
            fmt += "payload += "
        if len(buf) - i >= 64:
            fmt += f"\"{buf[i:i+64]}\"\n"
        else:
            fmt += f"\"{buf[i:]}\"\n"
        i += 64
    print(fmt)

def print_payload_metadata(payload: bytes):
    """ Prints additional information about the payload. """
    contains_nulls = b"\x00" in payload
    contains_tabs = b"\x09" in payload
    contains_lf = b"\x0a" in payload
    contains_cr = b"\x0d" in payload
    contains_spaces = b"\x20" in payload
    contains_signed = False
    for char in payload:
        if char >= 128:
            contains_signed = True
            break
    print(f"\t{YEL}--==[ Payload Metadata ]==--{NON}\n")
    print_key_val("Size", len(payload))
    print_key_val("Contains Nulls", format_bool(contains_nulls))
    print_key_val("Contains CR", format_bool(contains_cr))
    print_key_val("Contains LF", format_bool(contains_lf))
    print_key_val("Contains Spaces", format_bool(contains_spaces))
    print_key_val("Contains Tabs", format_bool(contains_tabs))
    print_key_val("Contains Signed Chars", format_bool(contains_signed))

    print("")

def print_payload_data(payload: bytes, args: argparse.Namespace):
    """
    Pretty printer function for the payload.  This will collect some
    basic data regarding the payload such as size and if contains nulls,
    spaces, newlines, carriage returns and prints this information before
    printing a backslash-x style hex encoded string of the payload.
    """
    print_payload_metadata(payload)
    # Hex-encode the string.
    buf = ""
    for char in payload:
        buf += f"\\x{char:02x}"

    # Print out the payload.
    print(f"\t{YEL}--==[ Payload Dump ]==--{NON}\n")
    if args.style.lower() == "c":
        print_c_payload(payload, buf, args)
    elif args.style.lower() == "python":
        print_python_payload(payload, buf, args)
    else:
        print(buf)

########################################################################
#                          SANITY FUNCTIONS
########################################################################
def which(binary: str) -> str:
    """
    This function is designed to emulate the Linux which command. It
    will grab the PATH environment variable and step through each path
    and look for the target binary. If found it will ensure that it
    is marked with the execute permission. If so it will return the
    full path to that binary, otherwise it will keep search. If not
    found, None will be returned.
    """
    for path in os.getenv('PATH').split(os.path.pathsep):
        needle = os.path.join(path, binary)
        if os.path.exists(needle) and os.access(needle, os.X_OK):
            return needle
    return ""

def sane_environment() -> bool:
    """
    Performs sanity checks of the build environment and ensures we have
    the required tools.
    """
    requirements = ['as', 'objcopy']
    for target in requirements:
        print_info(f"Checking {YEL}{target}{NON} is installed: ", end="")
        if not which(target):
            print(f"{RED}NOT FOUND{NON}")
            return False
        print(f"{GRN}FOUND{NON}")

    return True

########################################################################
#                       BUILD & EXTRACT FUNCTIONS
########################################################################
def build_and_extract_payload(src_path: str) -> bytes:
    """
    Builds the src file in the temp directory and attempts to extract
    the .text section of the binary as a raw binary array.
    """
    # Create a temp directory.
    dirpath = tempfile.mkdtemp()
    print_info("Compiling and extracting payload...")

    # Set some path variables for convinence.
    base_name = os.path.basename(src_path)
    src_tmp_path = os.path.join(dirpath, base_name)
    obj_tmp_path = os.path.join(dirpath, f"{base_name[:-2]}.o")
    payload_tmp_path = os.path.join(dirpath, "payload.bin")

    # Copy the Source code file to the directory.
    copy(src_path, dirpath)

    # Build the binary object using GAS.
    cmd = []
    cmd.append(which('as'))
    cmd.append('--march=i386')
    cmd.append('--32')
    cmd.append(src_tmp_path)
    cmd.append('-o')
    cmd.append(obj_tmp_path)

    # Check that the object file was created or abort.
    if execute_command(cmd) != 0 or not os.path.exists(obj_tmp_path):
        print_error("Compilation failed, object file was not created.")
        sys.exit(4)

    # Use objcopy to extract the .text section of the object.
    cmd = []
    cmd.append(which('objcopy'))
    cmd.append('-j')
    cmd.append('.text')
    cmd.append('-O')
    cmd.append('binary')
    cmd.append(obj_tmp_path)
    cmd.append(payload_tmp_path)
    execute_command(cmd)

    # Check that the payload file was created or abort.
    if execute_command(cmd) != 0 or not os.path.exists(payload_tmp_path):
        print_error("Objcopy failed, payload file was not created.")
        sys.exit(5)

    # open and extract the payload contents.
    with open(payload_tmp_path, 'rb') as fil:
        payload = fil.read()

    # Check that the payload has some sort of size or abort.
    if len(payload) == 0:
        print_error("Payload extraction failed, Payload was zero bytes.")
        sys.exit(6)

    # otherwise, return the extracted payload.
    print_success("\033[32;1mPayload extraction complete!\033[0m\n")
    return payload

def execute_command(cmd: list) -> int:
    """
    Use subprocess.Popen() to execute a command and return it's exit
    code.
    """
    try:
        proc = subprocess.Popen(cmd)
        exitcode = proc.wait()
    except OSError:
        print_error(f"Unable to execute build command {cmd[0]}")
        sys.exit(3)
    return exitcode

def parse_arguments() -> argparse.Namespace:
    """ Configure argparse and get arguments. """
    desc = "This tool will build and extract a GAS x86 source file and "
    desc += "attempt to extract a raw binary copy of the .text section "
    desc += "of the object it compiled and print it in a formatted manner."

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('src_file', type=str,
                        help='The target x86 GAS src file')

    desc = 'Format for output. Can be "raw", "python", or "c". Default is "raw"'
    parser.add_argument('--style', '-s', type=str, default="raw",
                        help=desc)

    # If the user provided no arguments, just print the help screen.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # check that the style argument is valid.
    if args.style.lower() not in ["raw", "python", "c"]:
        print_error(f"Invalid style specified: {args.style}\n")
        parser.print_help()
        sys.exit(1)

    # Check that src file path is valid.
    if not os.path.exists(args.src_file):
        print_error("Invalid path to source file.\n")
        parser.print_help()
        sys.exit(1)

    print_success("Payload extraction complete.")
    return args

def main():
    """ Main Application Logic. """
    # Print a banner.
    print(f"\n\t{YEL}---===[ {TITLE} {VERSION} ]===---{NON}\n")

    # Get the arguments
    args = parse_arguments()

    # Sanity check that the tools we need are installed on the OS.
    if not sane_environment():
        return 2

    # Start the extraction process.
    payload = build_and_extract_payload(args.src_file)

    # Print out payload and metadata.
    print_payload_data(payload, args)

    return 0

if __name__ == "__main__":
    sys.exit(main())
