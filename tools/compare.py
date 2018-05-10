import difflib
import sys


def compare_file_content(from_file_path, to_file_path):
    with open(from_file_path, 'r') as from_file, open(to_file_path, 'r') as to_file:
        file_diff = difflib.unified_diff(
            from_file.readlines(),
            to_file.readlines(),
            fromfile='FromFile',
            tofile='ToFile',
            lineterm='')
        return [line for line in file_diff]


if __name__ == '__main__':
    src_file_path = sys.argv[1]
    dst_file_path = sys.argv[2]

    diff_lines = compare_file_content(from_file_path=dst_file_path, to_file_path=src_file_path)
    if diff_lines:
        print('\n'.join(diff_lines))
        exit(1)
    else:
        exit(0)
