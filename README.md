A python script that creates a zip file without timestamp metadata, adding all files and directories in the current working directory into it. Note that some extraction programs may parse the zero byte in the date and time field as December 31st, 1979, while others may interpret it as having no timestamp.

## Usage
`cd` first to the directory to zip before running pycleanzip.
```sh
python3 /path/to/pycleanzip.py -o out.zip
```
`-o` parameter is optional, defaults to `file.zip`.
