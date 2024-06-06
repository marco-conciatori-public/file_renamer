import os
import shutil
from tkinter import *
from datetime import datetime
from tkinter import filedialog


def pretty_print_dict(data, _level: int = 0):
    if type(data) == dict:
        for key in data:
            for i in range(_level):
                print('\t', end='')
            print(f'{key}:')
            pretty_print_dict(data[key], _level=_level + 1)
    else:
        for i in range(_level):
            print('\t', end='')
        print(data)


def get_args_gui() -> dict:
    # create root window
    root = Tk()
    # root window title and dimension
    root.title("File Renamer")
    root.geometry('560x250')
    # root.configure()

    input_frame = Frame(root)
    input_frame.pack(side=TOP, fill=BOTH, expand=True)

    columnspan = 4
    pady = 10
    # input_folder_path
    row = 0
    Label(input_frame, text="Path to the video folder:").grid(column=0, row=row)
    input_folder_path = StringVar(input_frame, value='Select folder')

    def browse_input_folders():
        folder_path = filedialog.askdirectory(initialdir="/", title="Select a Folder")
        input_folder_path.set(folder_path)
    Entry(input_frame, width=40, textvariable=input_folder_path).grid(column=1, row=row, columnspan=columnspan, padx=10)
    Button(input_frame, text="Browse", command=browse_input_folders).grid(column=2 + columnspan, row=row)

    # output_folder_path
    row += 1
    Label(input_frame, text="Path to destination folder: \n(Leave empty to use the same as input)").grid(column=0, row=row)
    output_folder_path = StringVar(input_frame, value='Leave empty to use the same as input')

    def browse_output_folders():
        folder_path = filedialog.askdirectory(initialdir="/", title="Select a Folder")
        output_folder_path.set(folder_path)
    Entry(input_frame, width=40, textvariable=output_folder_path).grid(column=1, row=row, columnspan=columnspan, padx=10)
    Button(input_frame, text="Browse", command=browse_output_folders).grid(column=2 + columnspan, row=row)

    # name_prefix
    row += 2
    Label(input_frame, text="Prefix for file names (optional):").grid(column=0, row=row, pady=pady)
    name_prefix = StringVar(input_frame, value='')
    Entry(input_frame, width=40, textvariable=name_prefix).grid(column=1, row=row, columnspan=columnspan)

    # name_suffix
    row += 1
    Label(input_frame, text="Suffix for file names (optional):").grid(column=0, row=row, pady=pady)
    name_suffix = StringVar(input_frame, value='')
    Entry(input_frame, width=40, textvariable=name_suffix).grid(column=1, row=row, columnspan=columnspan)

    # convert_only_format
    # row += 1
    # Label(input_frame, text="Convert only the following formats (optional):").grid(column=0, row=row)
    # convert_only_format = StringVar(input_frame, value='')
    # Entry(input_frame, width=40, textvariable=convert_only_format).grid(column=1, row=row)

    # keep_original
    row += 1
    Label(input_frame, text="Keep original files?").grid(column=0, row=row, pady=pady)
    keep_original_int = IntVar(input_frame, value=0)
    Radiobutton(input_frame, text="Yes", value=1, variable=keep_original_int).grid(column=1, row=row)
    Radiobutton(input_frame, text="No", value=0, variable=keep_original_int).grid(column=2, row=row)

    # verbose
    # row += 1
    # Label(input_frame, text="Verbose?").grid(column=0, row=row)
    # verbose_int = IntVar(input_frame, value=0)
    # Radiobutton(input_frame, text="Yes", value=1, variable=verbose_int).grid(column=1, row=row)
    # Radiobutton(input_frame, text="No", value=0, variable=verbose_int).grid(column=2, row=row)
    # verbose = bool(verbose_int.get())

    control_frame = Frame(root)
    control_frame.pack(side=BOTTOM, fill=X, expand=False)

    # ok and cancel buttons
    Button(control_frame, text="OK", width=10, command=root.destroy).pack(side=LEFT, padx=135, pady=pady)
    Button(control_frame, text="Cancel", width=10, command=root.destroy).pack(side=LEFT, padx=0)

    # all widgets will be here
    # Execute Tkinter
    root.mainloop()

    if output_folder_path.get() == 'Leave empty to use the same as input' or output_folder_path.get() == '':
        output_folder_path.set(input_folder_path.get())
    args_dict = {
        'input_folder_path': input_folder_path.get(),
        'output_folder_path': output_folder_path.get(),
        'name_prefix': name_prefix.get(),
        'name_suffix': name_suffix.get(),
        'convert_only_format': [],
        'keep_original': bool(keep_original_int.get()),
        'verbose': True,
    }
    pretty_print_dict(args_dict)

    return args_dict


def rename_files(**kwargs):
    input_folder_path = kwargs['input_folder_path']
    output_folder_path = kwargs['output_folder_path']
    if input_folder_path[-1] != '/':
        input_folder_path += '/'
    if output_folder_path[-1] != '/':
        output_folder_path += '/'
    name_prefix = kwargs['name_prefix']
    name_suffix = kwargs['name_suffix']
    if name_prefix != '':
        if name_prefix[-1] != '_':
            name_prefix += '_'
    if name_suffix != '':
        if name_suffix[0] != '_':
            name_suffix = f'_{name_suffix}'
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
        print(f' - Keep original files: {keep_original}')
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
    kwargs = get_args_gui()
    rename_files(**kwargs)
