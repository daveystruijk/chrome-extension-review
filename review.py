import os
import glob2
import json
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
    current_dir = versions[0]
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
    print(name)

