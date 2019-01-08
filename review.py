import os
import glob2
import json
import shutil
from subprocess import call
from pprint import pprint


# For MacOS: /Users/<username>/Library/Application Support/Google/Chrome/Profile 1/Extensions
extensions_dir = os.getenv('CHROME_EXTENSIONS_DIR')

def find_directories(directory):
    return [d for d in glob2.glob(directory + '/*' ) if os.path.isdir(d)]

def load_messages_file(directory):
    locale_dirs = find_directories(directory + '/_locales')
    messages_file = ''
    for locale_dir in locale_dirs:
        if 'en' in os.path.basename(locale_dir):
            messages_file = locale_dir + '/messages.json'
            break
    with open(messages_file) as f:
        messages = json.load(f)
    return messages

directories = find_directories(extensions_dir)

for directory in directories:
    versions = find_directories(directory)
    if not versions:
        continue
    print(directory)
    current_dir = sorted(versions)[-1]
    with open(current_dir + '/manifest.json') as f:
        manifest = json.load(f)
    name = manifest['name']
    if '__MSG_' in name:
        messages = load_messages_file(current_dir)
        #pprint(messages)
        search_string = name.replace('__MSG_', '').replace('__', '')
        for key, value in messages.items():
            if key.lower() == search_string.lower():
                name = value['message']

    save_path = os.getcwd() + '/extensions/' + name

    if os.path.isdir(save_path + '/.git'):
        shutil.move(save_path + '/.git', os.getcwd() + '/.tempgit')
        shutil.rmtree(save_path)
        shutil.copytree(current_dir + '/', save_path)
        shutil.move(os.getcwd() + '/.tempgit', save_path + '/.git')
        call(["git", "status"], cwd=save_path)
    else:
        shutil.copytree(current_dir + '/', save_path)
        call(["git", "init"], cwd=save_path)
        call(["git", "add", "--all"], cwd=save_path)
        call(["git", "commit", "-m", "Initial commit"], cwd=save_path)
