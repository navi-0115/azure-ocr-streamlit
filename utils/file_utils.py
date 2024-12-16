import os

def secure_filename(filename):
    return os.path.basename(filename).replace(" ", "_")
