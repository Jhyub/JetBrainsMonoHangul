import zipfile
import os
import shutil
import sys

from config import *
from hangulify import build_font

if not use_system_wget:
    import wget

def usage():
    print(f'python {sys.argv[0]} <subcommand>')
    print(f'')
    print(f'subcommand:')
    print(f'    all: automatically setup and build fonts.')
    print(f'    setup: download needed files and extract from zip.')
    print(f'    build: outputs merged fonts.')
    print(f'    clean: remove all output files including downloaded files.')

if len(sys.argv) == 1:
    usage()
    exit(1)

subcommand = sys.argv[1]

def setup():
    print('[INFO] Download font files')

    print('[INFO] Download JetBrains Mono')
    if not use_system_wget:
        wget.download(jetbrains_mono_url, out=jetbrains_mono_name);
    else:
        os.system(f'wget {jetbrains_mono_url} -O {jetbrains_mono_name}')
    print()

    print('[INFO] Download D2 Coding')
    if not use_system_wget:
        wget.download(d2_coding_url, out=d2_coding_name);
    else:
        os.system(f'wget {d2_coding_url} -O {d2_coding_name}')
    print()

    if not os.path.exists(download_path):
        print(f'[INFO] Make \'{download_path}\' directory')
        os.makedirs(download_path)

    print('[INFO] Move downloaded font files into assets directory')
    shutil.move(f'./{jetbrains_mono_name}', f'{download_path}/')
    shutil.move(f'./{d2_coding_name}', f'{download_path}/')

    print('[INFO] Extract JetBrains Mono from zip file')
    with zipfile.ZipFile(f'{download_path}/{jetbrains_mono_name}', 'r') as zip_ref:
        zip_ref.extractall(download_path)

    print('[INFO] Extract D2 Coding from zip file')
    with zipfile.ZipFile(f'{download_path}/{d2_coding_name}', 'r') as zip_ref:
        zip_ref.extractall(download_path)

def clean():
    print('[INFO] Remove downloaded files')
    shutil.rmtree(download_path)

    print('[INFO] Remove output files')
    shutil.rmtree(out_path)

if subcommand == 'all':
    print('[INFO] Remove remaining files')
    try:
        clean()
    except:
        print('[INFO] No output files found.')
    print('[INFO] Download and extract from zip')
    setup()
    print('[INFO] Build fonts')
    build_font()
if subcommand == 'setup':
    setup()
elif subcommand == 'build':
    build_font()
elif subcommand == 'clean':
    clean()
else:
    usage()
    exit(1)
