import difflib
import sys


def compare_files(from_file_path, to_file_path):
    with open(from_file_path, 'r') as from_file:
        with open(to_file_path, 'r') as to_file:
            differ = difflib.Differ()
            diff = differ.compare(from_file.readlines(), to_file.readlines())
            print('\n'.join(diff))


def compare_files_detailed(from_file_path, to_file_path):
    with open(from_file_path, 'r') as from_file:
        with open(to_file_path, 'r') as to_file:
            for line in difflib.unified_diff(from_file.readlines(),
                                             to_file.readlines(),
                                             fromfile=from_file_path,
                                             tofile=to_file_path,
                                             lineterm='',
                                             n=0):
                for prefix in ('---', '+++', '@@'):
                    if line.startswith(prefix):
                        break
                else:
                    print(line)


def main():
    src_file_path = sys.argv[1]
    dst_file_path = sys.argv[2]

    # compare_files(from_file_path=dst_file_path, to_file_path=src_file_path)
    compare_files_detailed(from_file_path=dst_file_path, to_file_path=src_file_path)


if __name__ == '__main__':
    main()
