#!/usr/bin/env python3
import os
import re

cur_path = os.path.dirname(os.path.realpath(__file__))
opendbc_root = os.path.join(cur_path, '../')
include_pattern = re.compile(r'CM_ "IMPORT (.*?)";')


def read_dbc(src_dir, filename):
  with open(os.path.join(src_dir, filename)) as file_in:
    return file_in.read()


def create_dbc(src_dir, filename, output_path):
  dbc_file_in = read_dbc(src_dir, filename)

  includes = include_pattern.findall(dbc_file_in)

  output_filename = filename.replace('.dbc', '_generated.dbc')
  output_file_location = os.path.join(output_path, output_filename)

  with open(output_file_location, 'w') as dbc_file_out:
    dbc_file_out.write('CM_ "AUTOGENERATED FILE, DO NOT EDIT";\n')

    for include_filename in reversed(includes):
      include_file_header = '\n\nCM_ "Imported file %s starts here";\n' % include_filename
      dbc_file_out.write(include_file_header)

      include_file = read_dbc(src_dir, include_filename)
      dbc_file_out.write(include_file)

    dbc_file_out.write('\nCM_ "%s starts here";\n' % filename)

    core_dbc = include_pattern.sub('', dbc_file_in)
    dbc_file_out.write(core_dbc)


def create_all(output_path):
  for src_dir, _, filenames in os.walk(cur_path):
    if src_dir == cur_path:
      continue

    #print(src_dir)
    for filename in filenames:
      if filename.startswith('_') or not filename.endswith('.dbc'):
        continue

      #print(filename)
      create_dbc(src_dir, filename, output_path)

if __name__ == "__main__":
  create_all(opendbc_root)