FROM python:3.10-slim 
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "Problem1/main.py", "--spec_file_path", "spec.json", "--fixed_width_file_path", "sample_fixed_width_file", "--delimiter", ",", "--delimiter_file_path", "sample_delimiter"]

