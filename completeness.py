import pygrib
import pandas as pd
import os
import os.path


def completeness():
    drct = './dataset/'
    files = os.listdir('./dataset')
    sorted_files = sorted(files)

    k=0
    error_files=[]
    for filename in sorted_files:
        grbs = pygrib.open(drct+filename)
        count = len(grbs.read())
        if count!=3:
            error_files.append(filename)
        k+=1
        if k%100 == 0:
            print('{} files passed'.format(k))
        
    return error_files

# if __name__ == '__main__':
#     completeness()