FROM python:3.9
WORKDIR /app
COPY . /app
RUN python -m unittest discover -s . -p "test.py"
CMD ["python", "Problem1/main.py", "--spec_file_path", "spec.json", "--fixed_width_file_path", "sample_fixed_width_file", "--delimiter", ",", "--delimiter_file_path", "sample_delimiter"]