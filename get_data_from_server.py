import os
import ftplib

def create_folder():
    pwd = os.getcwd()
    if not pwd.split('/')[-1] == 'data':
        if not 'data' in os.listdir(pwd):
            os.mkdir('data')
        os.chdir(fr'{pwd}/data')

def download():
    ftp = ftplib.FTP('website', 'login', 'password')
    file = 'product_list_932.xml'
    try:
        with open(file, 'wb') as f:
            ftp.retrbinary(f'RETR {file}', f.write)
    except ftplib.error_perm:
        exit()
    ftp.quit()

if __name__ == '__main__':
    create_folder()
    download()
