# MoufaDNS

These scripts implement a fake DNS where a computer's IP is written in a Google Drive folder with `ip_writer.py` and read from another with `ip_reader.py`. 

If allowed, the `ip_reader.py` script will write the IP on the hosts file, with the hostname being the name of the file on Google Drive, thus implementing a "fake DNS".
