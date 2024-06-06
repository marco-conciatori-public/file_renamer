import os
import copy
import shutil
import argparse
from datetime import datetime


def read_command_line_args(default_args_dict: dict) -> dict:
    parser = argparse.ArgumentParser()
    for key in default_args_dict:
        value = default_args_dict[key]
        if isinstance(value, list):
            parser.add_argument(f'--{key}', dest=key, type=str, nargs='*')
        elif isinstance(value, bool):
            parser.add_argument(f'--{key}', dest=key, default=value, action='store_true')
        else:
            parser.add_argument(f'--{key}', dest=key, type=type(value))

    args = parser.parse_args()
    args_dict = vars(args)
    updated_args_dict = copy.deepcopy(default_args_dict)
    for key in args_dict:
        if args_dict[key] is not None:
            updated_args_dict[key] = args_dict[key]
    return updated_args_dict


def get_args(default_args_dict: dict) -> dict:
    args_dict = read_command_line_args(default_args_dict=default_args_dict)
    temp_args_dict = copy.deepcopy(args_dict)

    input_folder_path = args_dict['input_folder_path']
    if input_folder_path == '':
        input_folder_path = input('Insert path to the video folder:')
    output_folder_path = args_dict['output_folder_path']
    if output_folder_path == '':
        output_folder_path = input('Insert path to the output folder (press enter to use the same as input):')
    if output_folder_path == '':
        output_folder_path = input_folder_path
    name_prefix = args_dict['name_prefix']
    if name_prefix == '':
        name_prefix = input('Insert prefix for file names (press enter to skip):')
    if name_prefix != '':
        if name_prefix[-1] != '_':
            name_prefix += '_'
    name_suffix = args_dict['name_suffix']
    if name_suffix == '':
        name_suffix = input('Insert suffix for file names (press enter to skip):')
    if name_suffix != '':
        if name_suffix[0] != '_':
            name_suffix = f'_{name_suffix}'
    convert_only_format = args_dict['convert_only_format']
    new_convert_only_format = []
    for file_format in convert_only_format:
        new_convert_only_format.append(file_format.lower())
    convert_only_format = new_convert_only_format
    keep_original = args_dict['keep_original']
    keep_original_str = ('Keep original files? (y/n):')
    if keep_original_str.lower() == 'y' or keep_original_str.lower() == 'yes':
        keep_original = True

    temp_args_dict['input_folder_path'] = input_folder_path
    temp_args_dict['output_folder_path'] = output_folder_path
    temp_args_dict['name_prefix'] = name_prefix
    temp_args_dict['name_suffix'] = name_suffix
    temp_args_dict['convert_only_format'] = convert_only_format
    temp_args_dict['keep_original'] = keep_original
    return temp_args_dict


def rename_files(**kwargs):
    input_folder_path = kwargs['input_folder_path']
    output_folder_path = kwargs['output_folder_path']
    name_prefix = kwargs['name_prefix']
    name_suffix = kwargs['name_suffix']
    convert_only_format = kwargs['convert_only_format']
    keep_original = kwargs['keep_original']
    if kwargs['verbose']:
        print('File renamer is running...')
        print(f' - Select files from: {input_folder_path}')
        print(f' - Put renamed files in: {output_folder_path}')
        if name_prefix != '':
            print(f' - Prefix added to all file names: {name_prefix}')
        if name_suffix != '':
            print(f' - Suffix added to all file names: {name_suffix}')
        if len(convert_only_format) > 0:
            print(f' - Convert only the following formats: {convert_only_format}')
        print(f' - Keep original file/s: {keep_original}')
    counter = 0
    with os.scandir(input_folder_path) as dir_entry_iterator:
        for entry in dir_entry_iterator:
            if entry.is_file():
                file_format = entry.name.split('.')[-1]
                file_format = file_format.lower()
                if file_format not in convert_only_format and len(convert_only_format) > 0:
                    continue

                birth_time = entry.stat().st_birthtime
                datetime_birth_time = datetime.fromtimestamp(birth_time)
                time_stamp = datetime_birth_time.strftime('%Y-%m-%d_%H-%M-%S')

                new_file_name = f'{name_prefix}{time_stamp}{name_suffix}.{file_format}'

                if keep_original:
                    shutil.copy(src=entry.path, dst=f'{output_folder_path}{new_file_name}')
                else:
                    os.rename(src=entry.path, dst=f'{output_folder_path}{new_file_name}')
                counter += 1

    if kwargs['verbose']:
        print(f'Execution completed: {counter} files have been renamed.')


if __name__ == '__main__':
    kwargs = {
        'input_folder_path': '',
        'output_folder_path': '',
        'name_prefix': '',
        'name_suffix': '',
        'convert_only_format': [],
        'keep_original': False,
        'verbose': True,
    }
    # D:/GIT/file_renamer/data/
    updated_kwargs = get_args(default_args_dict=kwargs)
    rename_files(**updated_kwargs)
    input('Press any key to exit...')
