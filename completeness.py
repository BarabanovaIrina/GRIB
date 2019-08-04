import pygrib
import os
import os.path


def completeness(directory):
    # directory = './'
    files = os.listdir(directory)
    sorted_files = sorted(files)

    k = 0
    error_files = []
    for filename in sorted_files:
        gribs = pygrib.open(f"{directory}/{filename}")
        count = len(gribs.read())
        if count != 3:
            error_files.append(filename)
        k += 1
        if k % 100 == 0:
            print(f"{k} files passed")

    return error_files

# if __name__ == '__main__':
#     completeness()
