import os
import shutil
import tkinter as tk
from tkinter import *
from datetime import datetime
from tkinter import filedialog


def show_tooltip(window, text: str):
    # Create a new top-level window with the tooltip text
    window.tooltip_window = tk.Toplevel(window)
    tooltip_label = tk.Label(
        window.tooltip_window,
        text=text,
        wraplength=300,
        justify='left',
        bg='lightyellow',
        padx=10,
        pady=5,
    )
    tooltip_label.pack()

    # Use the overrideredirect method to remove the window's decorations
    window.tooltip_window.overrideredirect(True)

    # Calculate the coordinates for the tooltip window
    x = window.winfo_pointerx() + 20
    y = window.winfo_pointery() + 20
    window.tooltip_window.geometry('+{}+{}'.format(x, y))


def hide_tooltip(window):
    # Destroy the tooltip window
    window.tooltip_window.destroy()
    window.tooltip_window = None


def add_text_to_string_var(string_var, text):
    temp_text = string_var.get()
    if temp_text == '':
        string_var.set(text)
    else:
        string_var.set(f'{temp_text}\n{text}')


def file_renamer_gui_():
    # create root window
    root = Tk()
    # root window title and dimension
    root.title('File Renamer')
    # root window icon
    # root.iconbitmap('resources/images/icon_1.ico')
    # root window min size
    root.minsize(width=450, height=355)

    columnspan = 4
    pady = 10
    padx = 10

    # add global left padding
    Frame(root, width=10).pack(side=LEFT, fill=X, expand=False)
    # add global right padding
    Frame(root, width=10).pack(side=RIGHT, fill=X, expand=False)

    # FRAME 1
    input_frame = Frame(root)
    input_frame.pack(side=TOP, fill=X, expand=False)

    # input_folder_path
    row = 0
    label_input_path = Label(input_frame, text='Path to the video folder:')
    label_input_path.grid(column=0, row=row, sticky=W, pady=pady)
    input_path_tooltip = 'Select the folder where the files are located.'
    label_input_path.bind("<Enter>", lambda event: show_tooltip(window=root, text=input_path_tooltip))
    label_input_path.bind("<Leave>", lambda event: hide_tooltip(window=root))
    input_folder_path = StringVar(input_frame, value='')

    def browse_input_folders():
        folder_path = filedialog.askdirectory(initialdir='/', title='Select a Folder', mustexist=True)
        input_folder_path.set(folder_path)
    Entry(input_frame, width=40, textvariable=input_folder_path).grid(
        column=1,
        row=row,
        columnspan=columnspan,
        padx=10,
        pady=pady,
    )
    Button(input_frame, text='Browse', command=browse_input_folders).grid(
        column=2 + columnspan,
        row=row,
        pady=pady,
        padx=padx,
    )

    # output_folder_path
    row += 1
    label_output_path = Label(input_frame, text='Path to destination folder: (optional)')
    label_output_path.grid(column=0, row=row, sticky=W, pady=pady)
    output_path_tooltip = 'Select the folder where the renamed files will be saved. If not specified, the renamed ' \
                          'files will be saved in the same folder as the original files.'
    label_output_path.bind("<Enter>", lambda event: show_tooltip(window=root, text=output_path_tooltip))
    label_output_path.bind("<Leave>", lambda event: hide_tooltip(window=root))
    output_folder_path = StringVar(input_frame, value='')

    def browse_output_folders():
        folder_path = filedialog.askdirectory(initialdir='/', title='Select a Folder', mustexist=True)
        output_folder_path.set(folder_path)
    Entry(input_frame, width=40, textvariable=output_folder_path).grid(
        column=1,
        row=row,
        columnspan=columnspan,
        padx=10,
        pady=pady,
    )
    Button(input_frame, text='Browse', command=browse_output_folders).grid(
        column=2 + columnspan,
        row=row,
        pady=pady,
        padx=padx,
    )

    # name_prefix
    row += 1
    prefix_label = Label(input_frame, text='Prefix for file names (optional):')
    prefix_label.grid(column=0, row=row, pady=pady, sticky=W)
    prefix_tooltip = 'Add a prefix to the new file names. The prefix will be followed by the date and time' \
                     ' the file was created.'
    prefix_label.bind("<Enter>", lambda event: show_tooltip(window=root, text=prefix_tooltip))
    prefix_label.bind("<Leave>", lambda event: hide_tooltip(window=root))
    name_prefix = StringVar(input_frame, value='')
    Entry(input_frame, width=40, textvariable=name_prefix).grid(column=1, row=row, columnspan=columnspan, pady=pady)

    # name_suffix
    row += 1
    suffix_label = Label(input_frame, text='Suffix for file names (optional):')
    suffix_label.grid(column=0, row=row, pady=pady, sticky=W)
    suffix_tooltip = 'Add a suffix to the new file names. The suffix will be preceded by the date and time' \
                     ' the file was created.'
    suffix_label.bind("<Enter>", lambda event: show_tooltip(window=root, text=suffix_tooltip))
    suffix_label.bind("<Leave>", lambda event: hide_tooltip(window=root))
    name_suffix = StringVar(input_frame, value='')
    Entry(input_frame, width=40, textvariable=name_suffix).grid(column=1, row=row, columnspan=columnspan, pady=pady)

    # convert_only_format
    # row += 1
    # Label(input_frame, text='Convert only the following formats (optional):').grid(
    #     column=0,
    #     row=row,
    #     pady=pady,
    #     sticky=W,
    # )
    # convert_only_format = StringVar(input_frame, value='')
    # Entry(input_frame, width=40, textvariable=convert_only_format).grid(column=1, row=row, pady=pady)

    # keep_original
    row += 1
    keep_files_label = Label(input_frame, text='Keep original files?')
    keep_files_label.grid(column=0, row=row, pady=pady * 2, sticky=W)
    keep_files_tooltip = '"Yes": change name and location of copies of the original files, to keep them unchanged.' \
                         '\n"No": the original files will be renamed and moved to the destination folder.'
    keep_files_label.bind("<Enter>", lambda event: show_tooltip(window=root, text=keep_files_tooltip))
    keep_files_label.bind("<Leave>", lambda event: hide_tooltip(window=root))
    keep_original_int = IntVar(input_frame, value=0)
    Radiobutton(input_frame, text='Yes', value=1, variable=keep_original_int).grid(column=1, row=row, pady=pady * 2)
    Radiobutton(input_frame, text='No', value=0, variable=keep_original_int).grid(column=2, row=row, pady=pady * 2)

    # verbose
    # row += 1
    # Label(input_frame, text='Verbose?').grid(column=0, row=row, sticky=W)
    # verbose_int = IntVar(input_frame, value=0)
    # Radiobutton(input_frame, text='Yes', value=1, variable=verbose_int).grid(column=1, row=row)
    # Radiobutton(input_frame, text='No', value=0, variable=verbose_int).grid(column=2, row=row)
    # verbose = bool(verbose_int.get())

    # expand entry widget when window is resized
    # input_frame.grid_columnconfigure(index=0, weight=0, minsize=100)
    input_frame.grid_columnconfigure(index=1, weight=1, minsize=40)
    # input_frame.grid_columnconfigure(index=2, weight=1, minsize=50)
    # input_frame.grid_columnconfigure(index=2 + columnspan, weight=0, minsize=50)

    # FRAME 2
    control_frame = Frame(root)
    control_frame.pack(side=BOTTOM, fill=X, expand=False)

    def rename_files_local_args():
        try:
            rename_files(
                input_folder_path=input_folder_path.get(),
                output_folder_path=output_folder_path.get(),
                name_prefix=name_prefix.get(),
                name_suffix=name_suffix.get(),
                convert_only_format=[],
                keep_original=bool(keep_original_int.get()),
                verbose=True,
                console_output_channel=console_output_channel,
            )
        except Exception as e:
            add_text_to_string_var(string_var=console_output_channel, text=e)
        ok_button_handle.config(state=DISABLED)
    # ok and exit buttons
    ok_button_handle = Button(control_frame, text='OK', width=10, command=rename_files_local_args)
    ok_button_handle.pack(side=LEFT, padx=125, pady=pady)
    Button(control_frame, text='Exit', width=10, command=root.destroy).pack(side=LEFT, padx=0, pady=pady)

    # FRAME 3
    console_output_frame = Frame(root)
    console_output_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
    # Separator between input and output frames
    separator = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

    # label description
    Label(console_output_frame, text='Console output:', anchor=W).pack(side=TOP, fill=X, expand=False)
    # console output
    console_output_channel = StringVar(console_output_frame, value='')
    console_output_label = Label(
        console_output_frame,
        anchor=NW,
        bg='lightgrey',
        fg='black',
        borderwidth=5,
        relief='sunken',
        justify=LEFT,
        textvariable=console_output_channel,
        padx=5,
        pady=5,
    )
    console_output_label.pack(side=LEFT, fill=BOTH, expand=True)

    # all widgets will be here
    # Execute Tkinter
    root.mainloop()


def process_args(args_dict: dict) -> dict:
    input_folder_path = args_dict['input_folder_path']
    output_folder_path = args_dict['output_folder_path']
    console_output_channel = args_dict['console_output_channel']
    if not os.path.exists(input_folder_path):
        add_text_to_string_var(
            string_var=console_output_channel,
            text=f'ERROR: Input folder does not exists: "{input_folder_path}"'
                 f'\nProgram terminated. 0 files have been renamed.')
        return {}

    if output_folder_path == '':
        output_folder_path = input_folder_path
    else:
        if not os.path.exists(output_folder_path):
            add_text_to_string_var(
                string_var=console_output_channel,
                text=f'ERROR: Output folder does not exists: "{output_folder_path}"'
                     f'\nProgram terminated. 0 files have been renamed.')
            return {}

    if input_folder_path[-1] != '/':
        input_folder_path += '/'
    if output_folder_path[-1] != '/':
        output_folder_path += '/'
    name_prefix = args_dict['name_prefix']
    name_suffix = args_dict['name_suffix']
    if name_prefix != '':
        if name_prefix[-1] != '_':
            name_prefix += '_'
    if name_suffix != '':
        if name_suffix[0] != '_':
            name_suffix = f'_{name_suffix}'
    convert_only_format = args_dict['convert_only_format']
    keep_original = args_dict['keep_original']
    if args_dict['verbose']:
        add_text_to_string_var(string_var=console_output_channel, text='File Renamer is running...')
        add_text_to_string_var(string_var=console_output_channel, text='With settings:')
        add_text_to_string_var(string_var=console_output_channel, text=f' - Select files from: {input_folder_path}')
        add_text_to_string_var(string_var=console_output_channel, text=f' - Put renamed files in: {output_folder_path}')
        if name_prefix != '':
            add_text_to_string_var(
                string_var=console_output_channel,
                text=f' - Prefix added to all file names: {name_prefix}',
            )
        if name_suffix != '':
            add_text_to_string_var(
                string_var=console_output_channel,
                text=f' - Suffix added to all file names: {name_suffix}',
            )
        if len(convert_only_format) > 0:
            add_text_to_string_var(
                string_var=console_output_channel,
                text=f' - Convert only the following formats: {convert_only_format}',
            )
        add_text_to_string_var(string_var=console_output_channel, text=f' - Keep original files: {keep_original}')

    preprocessed_args_dict = {
        'input_folder_path': input_folder_path,
        'output_folder_path': output_folder_path,
        'name_prefix': name_prefix,
        'name_suffix': name_suffix,
        'convert_only_format': convert_only_format,
        'keep_original': keep_original,
        'verbose': args_dict['verbose'],
        'console_output_channel': console_output_channel,
    }
    return preprocessed_args_dict


def rename_files(**kwargs):
    processed_kwargs = process_args(kwargs)
    input_folder_path = processed_kwargs['input_folder_path']
    output_folder_path = processed_kwargs['output_folder_path']
    name_prefix = processed_kwargs['name_prefix']
    name_suffix = processed_kwargs['name_suffix']
    convert_only_format = processed_kwargs['convert_only_format']
    console_output_channel = processed_kwargs['console_output_channel']
    keep_original = processed_kwargs['keep_original']
    counter = 0
    if processed_kwargs['verbose']:
        add_text_to_string_var(string_var=console_output_channel, text='Converting files...')

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

                if processed_kwargs['verbose']:
                    add_text_to_string_var(
                        string_var=console_output_channel,
                        text=f'\t{entry.name} -> {new_file_name}',
                    )
                if keep_original:
                    shutil.copy(src=entry.path, dst=f'{output_folder_path}{new_file_name}')
                else:
                    os.rename(src=entry.path, dst=f'{output_folder_path}{new_file_name}')
                counter += 1

    if processed_kwargs['verbose']:
        add_text_to_string_var(
            string_var=console_output_channel,
            text=f'Execution completed: {counter} files have been renamed.',
        )


if __name__ == '__main__':
    file_renamer_gui_()
