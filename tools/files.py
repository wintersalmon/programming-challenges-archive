import json
import os


class AutoCreateFileDirectory(object):

    def __init__(self, original_function, *, mode=0o755):
        self._original_function = original_function
        self._mode = mode

    def __call__(self, path, *args, **kwargs):
        self.get_or_create_path(path, self._mode)
        self._original_function(path, *args, **kwargs)

    @classmethod
    def get_or_create_path(cls, path, mode):
        base_dir = os.path.dirname(path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, mode=mode)


class SkipIfPathExists(object):
    def __init__(self, original_function):
        self._original_function = original_function

    def __call__(self, path, *args, **kwargs):
        if os.path.exists(path):
            prefix = 'Skip'
        else:
            prefix = 'New'
            self._original_function(path, *args, **kwargs)

        print('{prefix:4}: {path}'.format(prefix=prefix, path=path))


@SkipIfPathExists
def create_empty_directory(file_path: str, *, mode=0o755):
    os.makedirs(file_path, mode=mode)


@SkipIfPathExists
@AutoCreateFileDirectory
def create_text_file(path, *, content=None, is_binary=False):
    if is_binary:
        file_type = 'wb'
    else:
        file_type = 'w'

    with open(path, file_type) as file:
        if content is not None:
            file.write(content)


@SkipIfPathExists
@AutoCreateFileDirectory
def lazy_create_text_file(path, *, lazy_content=None, is_binary=False):
    if is_binary:
        file_type = 'wb'
    else:
        file_type = 'w'

    with open(path, file_type) as file:
        if lazy_content is not None:
            file.write(lazy_content())


@SkipIfPathExists
@AutoCreateFileDirectory
def create_json_file(path, *, content=None):
    with open(path, 'w') as file:
        if content is not None:
            json.dump(content, file)
