import json
import string
import random
import argparse

class GenerateFixedWidthFile:
    """ generate fixed width class to read spec config file, generate dummy rows and exporting the fixed width file
    """
    
    # Declaring some class variables used through out the operations
    column_names:list               # column names of the fixed width file
    offsets:list                    # width of each column
    fixed_width_encoding:str        # encoding of the exported file
    include_header:str              # Acting as a flag to check if column names are required as header

    def read_file(self, spec_file_path: str) -> None:
        """Method to read spec json file, parse it and assign class variable required for generating the file

        Args:
            spec_file_path (str): path of the spec json file

        Raises:
            IndexError: Raised when ColumnNames key is not found in the json config file
            IndexError: Raised when Offsets key is not found in the json config file
            IndexError: Raised when FixedWidthEncoding key is not found in the json config file
            IndexError: Raised when IncludeHeader key is not found in the json config file
            FileNotFoundError: Raised when program not able to find the file at location supplied or file is not readable
        """
        try:
            # open json config file
            with open(spec_file_path, 'r') as spec_json_data:
                spec_file_config = json.load(spec_json_data)        # parsing the json file

                # check the each required key below exists in the json config file and assign to class varible else raise error
                if "ColumnNames" in spec_file_config:
                    self.column_names = spec_file_config.get("ColumnNames")
                else: 
                    raise IndexError("ColumnNames key not in json config")
                if "Offsets" in spec_file_config:
                    self.offsets = spec_file_config.get("Offsets")
                else: 
                    raise IndexError("Offsets key not in json config")
                if "FixedWidthEncoding" in spec_file_config:
                    self.fixed_width_encoding = spec_file_config.get("FixedWidthEncoding")
                else: 
                    raise IndexError("FixedWidthEncoding key not in json config")
                if "IncludeHeader" in spec_file_config:
                    self.include_header = spec_file_config.get("IncludeHeader")
                else: 
                    raise IndexError("IncludeHeader key not in json config")
        except FileNotFoundError:
            # raising file not found error when file is not present at supplied location or not readable
            print(f"{spec_file_path} is not found or invalid!")

    
    def random_char(self) -> str:
        """Generates a dummy from ascii lowercase letters randomly

        Returns:
            str: random lowercase ascii letter
        """
        return random.choice(string.ascii_lowercase)
        
    
    def create_content(self, no_of_rows: int) -> str:
        """ Generates data for fixed width file

        Args:
            no_of_rows (int): No of rows to be generated for fixed width file

        Returns:
            str: Data generated returned as string 
        """
        # let the main string be empty to append the processed data
        main_str = ''
        # process the header record if the flag is TRUE
        if self.include_header == 'True':
            # iterate through each index of column and offset to generate header with specific width
            for index in range(len(self.column_names)):
                # generated header appended to the main string
                # using ljust method to fill the remaining space in fixed width cell with empty space after using the column name as value
                main_str += self.column_names[index].ljust(int(self.offsets[index]))
        # generate the rows data as per the input
        for _ in range(no_of_rows):
            # let there be empty inside str which can re used for each row ieteration
            inside_str = ''
            # iterate through each index of column and offset to generate header with specific width
            for index in range(len(self.column_names)):
                # using returned random char filling the remainig space with ljust method with empty space for fixed width cell
                inside_str += self.random_char().ljust(int(self.offsets[index]))
            # appending each row processed to the main string with new line character
            main_str += '\n' + inside_str
        
        return main_str
    
    def write_file(self, content: str, file_name: str) -> None:
        """writes the content and generates a file with file_name and encoding provided

        Args:
            content (str): content to be written in the file
            file_name (str): file name to be created and content written to
        """
        # writing the content provided into a file
        try:
            # opening with file to write with encoding provided in the spec config file
            with open(file_name, 'w', encoding=self.fixed_width_encoding) as output_file:
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
    description="Script that generates fixed width file based on config file"
    )

    argpass.add_argument("--spec_file_path", required=True, type=str)
    argpass.add_argument("--fixed_width_file_path", required=True, type=str)
    args = argpass.parse_args()

    # defining local vars from arguments passed
    spec_file_path = args.spec_file_path
    fixed_width_file_path = args.fixed_width_file_path

    # initializing generate fixed width file class
    generate_file_init = GenerateFixedWidthFile()
    # validating and reading the json spec file
    generate_file_init.read_file(spec_file_path)
    # faking the number of rows of data
    content = generate_file_init.create_content(10)
    # exporting the fixed width file
    generate_file_init.write_file(content, fixed_width_file_path)
    



