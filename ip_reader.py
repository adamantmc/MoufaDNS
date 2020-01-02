import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import sys
import argparse

def get_drive_service():
    creds_file = "gdrive_creds"
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile(creds_file)

    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(creds_file)
    
    drive = GoogleDrive(gauth)

    return drive

def get_ip(drive_service, ip_filename):
    file_list = drive_service.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    
    ip_file = None

    for f in file_list:
        if f["title"] == ip_filename:
            ip_file = f
            ip_file.FetchContent()

    ip = ip_file.content.getvalue().decode('utf-8')

    return ip

def write_to_file(ip, hostname, filename="/etc/hosts"):
    
    content = ""
    try:
        with open(filename, "r") as f:
            content = f.read()

        content = content.splitlines()
    except Exception:
        pass
    
    # Remove previous entry - if any
    clean = []
    
    for line in content:
        if hostname not in line:
            clean.append(line)
    
    # Add entry
    clean.append("{}\t{}".format(ip, hostname))

    # Try to write back to file
    try:
        with open(filename, "w") as f:
            f.write("\n".join(clean))
    except Exception as e:
        sys.stderr.write("Could not write to {} file - Exception error: {}\n".format(filename, e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--hostname", help="Name of the computer whose IP is written in Google Drive. This name must be the name of the file where the IP is written. It will also be the name that will be written in the output file.", default="homePC")
    parser.add_argument("--output_file", help="Name of the output file where the IP will be written. Defaults to /etc/hosts - the hostname will then resolve to the written IP in the Google Drive file.", default="/etc/hosts")
    args = parser.parse_args()

    drive_ip_filename = args.hostname

    script_dir = os.path.dirname(__file__)
    if script_dir != "":
        os.chdir(script_dir)
    
    service = get_drive_service()
    ip = get_ip(service, drive_ip_filename)
    write_to_file(ip, drive_ip_filename, args.output_file)