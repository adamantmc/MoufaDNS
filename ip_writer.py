import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import argparse

IP_SERVICE = "https://ident.me"

def get_ip(url):
    response = requests.get(url)
    ip = response.text

    return ip

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

def write_ip(ip, drive_service, drive_ip_filename):
    drive_file = drive_service.CreateFile({"title": drive_ip_filename})
    drive_file.SetContentString(ip)
    drive_file.Upload()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--hostname", help="Name of the computer whose IP is written in Google Drive. This name will also be used as the filename where the IP will be stored.", default="homePC")
    args = parser.parse_args()

    drive_ip_filename = args.hostname

    script_dir = os.path.dirname(__file__)
    if script_dir != "":
        os.chdir(script_dir)
    
    ip = get_ip(IP_SERVICE)
    service = get_drive_service()
    write_ip(ip, service, drive_ip_filename)