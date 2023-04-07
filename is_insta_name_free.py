#!/usr/bin/env python3

FILE_PREFIX = "/tmp/IINF_"

from typing import List

from bs4 import BeautifulSoup
import requests

def open_file(filename: str, check_not_empty=False) -> List[str]:
    filename = FILE_PREFIX + filename
    try:
        with open(filename, 'r', encoding='UTF-8') as f:
            file_contents = [line.strip('\n') for line in f]
    except FileNotFoundError:
        file_contents = []
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write('')

    if (check_not_empty) and (len(file_contents) == 0):
        print("%sPut some usernames into [%s] for fuck's sake%s" % ('\u001b[31;1m', filename, '\u001b[0m'))
        exit(-1)
    return file_contents

def is_free_username(username: str) -> bool:
    response = requests.get(f'https://www.instagram.com/{username}/')
    soup = BeautifulSoup(response.text, 'lxml')

    if(len(soup.text) > 73) :
        print("%sTAKEN: %s%s" % ('\u001b[31;1m', username, '\u001b[0m'))
        return False
    else:
        print("%sOK: %s%s" % ('\u001b[32;1m', username, '\u001b[0m'))
        return True

if __name__ == '__main__':
    not_taken_file = open(FILE_PREFIX + 'not_taken_usernames.txt', 'a', encoding='UTF-8')
    taken_file = open(FILE_PREFIX + 'taken_usernames.txt', 'a', encoding='UTF-8')

    not_taken_username_list = open_file('not_taken_usernames.txt')
    taken_username_list = open_file('taken_usernames.txt')
    username_list = open_file('usernames.txt', check_not_empty=True)

    for username in username_list:
        if (username not in not_taken_username_list) and (username not in taken_username_list):
            if is_free_username(username):
                not_taken_username_list.append(username)
                not_taken_file.write(username + '\n')
            else:
                taken_username_list.append(username)
                taken_file.write(username + '\n')

    # print all
    if len(taken_username_list) > 0:
        print("Taken:")
        for taken in taken_username_list:
            print("    " + taken)
    if len(not_taken_username_list) > 0:
        print("Free:")
        for not_taken in not_taken_username_list:
            print("    " + not_taken)
