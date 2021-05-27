import os
import zipfile
import argparse

argparser = argparse.ArgumentParser("Create a zip file from all the files in the working directory")
argparser.add_argument("-o", action="store", default="file.zip", help="output filename")
base_dir = os.curdir
zip_filename = argparser.parse_args().o

print("creating "+zip_filename+"' and adding '"+base_dir+"' to it")

def strip_zipinfo(zi):
    zi.date_time = (1980,0,0,0,0,0) # The final byte will become 0 after CPython does its bit manipulation
    zi.create_system = 3 # Unix
    zi.external_attr = None # Defaults to ?rw------- on CPython
    if zi.is_dir():
        zi.external_attr = 0o40775 << 16 # drwxrwxr-x, explicit default since CPython doesn't set the directory flag

with zipfile.ZipFile(zip_filename, "x", zipfile.ZIP_DEFLATED, False, 9) as zf:
    path = os.path.normpath(base_dir)
    if path != os.curdir:
        zf.write(path, path)
        print("adding "+path)
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for name in dirnames:
            path = os.path.normpath(os.path.join(dirpath, name))
            zi = zipfile.ZipInfo.from_file(path)
            strip_zipinfo(zi)
            zf.writestr(zi, bytes())
            print("adding "+path)
        for name in filenames:
            path = os.path.normpath(os.path.join(dirpath, name))
            if path != zip_filename and os.path.isfile(path):
                with open(path, "rb") as f:
                    zi = zipfile.ZipInfo.from_file(path)
                    strip_zipinfo(zi)
                    zf.writestr(zi, f.read(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
                    print("adding "+path)
