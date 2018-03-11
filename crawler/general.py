'''
Created on 30 de jan de 2018

@author: Bruno Queiroz
'''
import os
from _io import open
from main import PROJECT_NAME

def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Criando projeto " + directory)
        os.makedirs(directory)

def create_data_files(project_name, base_url):
    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name,"crawled.txt")
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, "")
        
def create_csv_file(project_name, eventsData):
    events = os.path.join(project_name, 'events.csv')
    if not os.path.isfile(events):
        write_file(events, eventsData)

def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)
    
    
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')
        
def delete_file_content(path):
    with open(path, 'w'):
        pass

def file_to_set(file_name):
    results = set()
    with open(file_name, 'r') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(links, file_name):
    with open(file_name, "w") as f:
        for l in sorted(links):
            f.write(l+"\n")
    