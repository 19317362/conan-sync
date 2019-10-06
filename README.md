# conan-sync

This is forked from (https://github.com/timdaman/conan-sync).

Many thanks to the auther.

This is a utility for sending all the contents of one conan(https://conan.io/) server to another. 
This is helpful when migrating to a new conan server or to create and maintain
a replica of a conan server.

This code is a quick and dirty solution I used to perform a server migration. 
Once that was done I stopped improving the code. The code does not perform
any deletions on any of the remotes and all modifications/uploads are
limited to the destination. 
 
I am offering this in the hopes it will save someone else time doing a 
similar task. I will accept patches to improve it.

## Memo (2019-10-06)
I'm in China. The network for conan center is very SLOW. And always timeout. To resolve this problem, I've tried to use this tool. But it can not work. I'm a C++ fan, not familiar with Python. The modification made by me maybe very ugly, but it works.

## Errors during my try

* The command "conan search -r server "*" " only works for conan-community
* Search and Dowload always timeout...
* Ctrl-C can make local recipe broken somehow....


## My solution

* sync all remote packages to local server for facility.
* split the process of download and upload
* add broken-fix while uploading


## How To Use (2019-10-06)
* run mydld_all.py to download with patern '*'
  ```python
  python3 mydld_all.py --source conan-center --dest my --ignore_failures
  ```
* run mydld.py to download with search each paterns from 'a' to 'z'
  ```python
  python3 mydld.py --source conan-center --dest my --ignore_failures
  ```
* run myup.py upload all local to my local server (will re-download broken recipes if any)
  ```python
  python3 myup.py --source conan-center --dest my --ignore_failures
  ```

