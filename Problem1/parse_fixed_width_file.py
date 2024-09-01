import json
import argparse

class ParseFixedWidthFile:

    # Declaring some class variables used through out the operations
    offsets:list                    # width of each column
    fixed_width_file_encoding:str        # encoding of the imported file
    delimited_file_encoding:str   # encoding used to export the delimited file

    def read_config_file(self, spec_file_path: str) -> None:
        """Method to read spec json file, parse it and assign class variable required for parsing the fixed width file 
        and generating the delimited file

        Args:
            spec_file_path (str): path of the spec json file

        Raises:
            IndexError: Raised when Offsets key is not found in the json config file
            IndexError: Raised when FixedWidthEncoding key is not found in the json config file
            IndexError: Raised when DelimitedEncoding key is not found in the json config file
            FileNotFoundError: Raised when program not able to find the file at location supplied or file is not readable
        """
        try:
            # open json config file
            with open(spec_file_path, 'r') as spec_json_data:
                spec_file_config = json.load(spec_json_data)        # parsing the json file

                # check the each required key below exists in the json config file and assign to class varible else raise error
                if "Offsets" in spec_file_config:
                    self.offsets = spec_file_config.get("Offsets")
                else: 
                    raise IndexError("Offsets key not in json config")
                if "FixedWidthEncoding" in spec_file_config:
                    self.fixed_width_file_encoding = spec_file_config.get("FixedWidthEncoding")
                else: 
                    raise IndexError("FixedWidthEncoding key not in json config")
                if "DelimitedEncoding" in spec_file_config:
                    self.delimited_file_encoding = spec_file_config.get("DelimitedEncoding")
                else: 
                    raise IndexError("DelimitedEncoding key not in json config")
        except FileNotFoundError:
            # rasing file not found error when file is not present at supplied location or not readable
            print(f"{spec_file_path} is not found or invalid!")
    
    def read_fixed_width_file(self, file_path: str) -> str:
        """This method can be used to read fixed width file based

        Args:
            file_path (str): path of the file to be read

        Returns:
            str: content of the file after read
        """
        try:
            # opening  the file in read only mode with supplied encoding in spec file to read
            with open(file_path, 'r', encoding=self.fixed_width_file_encoding) as fixed_width_file_content:
                # reading the file content
                file_content = fixed_width_file_content.read()
                return file_content
        except FileNotFoundError:
            # raising file not found error when file is not present at supplied location or not readable
            print(f"{file_path} is not found or invalid!")

    def parse_to_delimited(self, content: str, delimiter: str) -> str:
        """parsing the fixed width content to delimited format

        Args:
            content (str): fixed width content which needs to be parsed
            delimiter (str): delimiter to be used to seprate column attributes during parsing

        Returns:
            str: delimited content post parsing
        """
        try:
            # let there be empty main string, all processed rows will be appended to it.
            main_str = ''
            # procesing each row after spliting them on new line character
            for each_row in content.split("\n"):
                # let there be inside list, all column attributes after parsing appended to it
                inside_list = []
                # keep track of the offset when reading the column attribute
                offset_cntr = 0
                # looping through all the offset values to parse all the column level attribute present in a row
                for index in self.offsets:
                    index = int(index)
                    # appending the column level attribute to inside list, reading the row on char index [init offset to offset+index]
                    inside_list.append(each_row[offset_cntr:offset_cntr+index].strip()) 
                    # increment to offset value so that next column level attribute can be read
                    offset_cntr += index
                inside_str = f"{delimiter}".join(inside_list)       # use the delimiter passed to join the inside list to form a delimited string
                main_str += inside_str + '\n'                       # appending the parsed row to the main string
            return main_str
        except:
            raise

    def write_delimiter_file(self, content: str, file_name: str) -> None:
        """writes the content and generates a file with file_name and encoding provided

        Args:
            content (str): content to be written in the file
            file_name (str): file name to be created and content written to
        """
        # writing the content provided into a file
        try:
            # opening with file to write with encoding provided in the spec config file
            with open(file_name + ".csv", 'w', encoding=self.delimited_file_encoding) as output_file:
                try:
                    # writing the content
                    output_file.write(content)
                except (IOError, OSError):
                    # Catching exception when not able to write to file
                    print("Error writing to file")
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening file") 
    

if __name__ == '__main__':
    # passing required commandline arguments
    argpass = argparse.ArgumentParser(
        description="Script that parses fixed length file based on the config file"
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