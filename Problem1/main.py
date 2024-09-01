from generate_fixed_width_file import GenerateFixedWidthFile
from parse_fixed_width_file import ParseFixedWidthFile
import argparse

if __name__ == '__main__':
    # passing required commandline arguments
    argpass = argparse.ArgumentParser(
    description="Script that generates fixed width file based on config file and parse into the delimited file"
    )

    argpass.add_argument("--spec_file_path", required=True, type=str)
    argpass.add_argument("--fixed_width_file_path", required=True, type=str)
    argpass.add_argument("--delimiter", required=True, type=str)
    argpass.add_argument("--delimiter_file_path", required=True, type=str)
    args = argpass.parse_args()

    # defining local vars from arguments passed
    spec_file_path = args.spec_file_path
    fixed_width_file_path = args.fixed_width_file_path
    delimiter = args.delimiter
    delimiter_file_path = args.delimiter_file_path

    # initializing generate fixed width file class
    generate_file_init = GenerateFixedWidthFile()
    # validating and reading the json spec file
    generate_file_init.read_file(spec_file_path)
    # faking the number of rows of data
    content = generate_file_init.create_content(10)
    # exporting the fixed width file
    generate_file_init.write_file(content, fixed_width_file_path)


    # initialise the parse fixed width class
    parse_file_init = ParseFixedWidthFile()
    # reading the spec config file used to parse the file
    parse_file_init.read_config_file(spec_file_path)
    # reading fixed width file
    content = parse_file_init.read_fixed_width_file(fixed_width_file_path)
    # parsing the fixed width content to delimited content, providing delimiter here
    parsed_content = parse_file_init.parse_to_delimited(content, delimiter)
    # writing delimiter content to file 
    parse_file_init.write_delimiter_file(parsed_content, delimiter_file_path)