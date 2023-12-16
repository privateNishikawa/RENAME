import ctypes, os # , re
from glob import glob

def language_settings():
    kernel32 = ctypes.windll.kernel32
    system_language = kernel32.GetUserDefaultUILanguage()
    return system_language == 1041

def validate_path():
    global previous_path

    while True:
        folder_path = input("- ")
    
        if not folder_path and previous_path:
            return previous_path

        if folder_path and folder_path != 'a' and os.path.isdir(folder_path):
            previous_path = folder_path
            return folder_path
        else:
            print("\nE 有効なフォルダの絶対パスを入力してください。" if is_japanese else "\nE Please enter the absolute path of a valid folder.")

def count_folders(folder_path):
    folder_list = [f for f in glob(os.path.join(folder_path, '*')) if os.path.isdir(f) and not os.path.basename(f).startswith('.')]
    folder_count = len(folder_list)
    return folder_count

def count_files(folder_path):
    file_list = [folder_path] + [f for f in glob(os.path.join(folder_path, '*')) if os.path.isdir(f) and not os.path.basename(f).startswith('.')]
    file_count = sum(len(glob(os.path.join(file, '*'))) for file in file_list)
    folder_count = count_folders(folder_path)
    return file_count - folder_count

def rename_files(folder_path):
    global renamed_files
    folder_name = os.path.basename(folder_path)
    files = sorted(glob(os.path.join(folder_path, '*')), key=lambda x: os.path.getmtime(x)) # sorted(glob(os.path.join(folder_path, '*')), key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', os.path.basename(x))])
    retry_files = []

    for i, file_path in enumerate(files, start=1):
        if os.path.isfile(file_path):
            file_name, file_ext = os.path.splitext(os.path.basename(file_path))
            file_number = str(i)
            old_file_name = f"{file_name}{file_ext}"
            new_file_name = f"{folder_name}_{file_number}{file_ext}"

            while old_file_name != new_file_name:
                try:
                    os.rename(file_path, os.path.join(folder_path, new_file_name))
                    renamed_files += 1
                    print(f"+ No.{str(renamed_files).rjust(6)}: {old_file_name}  =>  {new_file_name}")
                    break
                except Exception:
                    retry_files.append((file_path, new_file_name))
                    break

    for file_path, new_file_name in retry_files:
        try:
            os.rename(file_path, os.path.join(folder_path, new_file_name))
            renamed_files += 1
            print(f"+ No.{str(renamed_files).rjust(6)}: {os.path.basename(file_path)} => {new_file_name}")
        except Exception as e:
            error_messages.append(f"E {os.path.basename(file_path)}: {str(e)}")

def main():
    global is_japanese, previous_path, renamed_files

    welcome_message = (
        "\n\nI ようこそ！.RENAME.exe をダウンロードしてくださり、ありがとうございます(o_ _)o\n"
        "  この実行ファイルは、C:ドライブ や SSD 、HDD などの大量のファイルが格納されているパスでの実行は推奨されません。\n"
        "  また、この実行ファイルのご利用によって生じたシステムエラーについては一切の責任を負いかねますことご了承ください。\n"
        "  実行ファイルを終了するには、右上の閉じるボタンをクリックするか、「Ctrl + C」を押してください。\n\n"
        if is_japanese else
        "\n\nI Welcome! Thank you for downloading .RENAME.exe :D\n"
        "  Running this executable in paths with a large number of files on C: drive, SSD, HDD, etc., is not recommended.\n"
        "  Also, please be aware that we cannot take responsibility for any system errors caused by using this executable.\n"
        "  To exit the program, click the close button at the top right or press 'Ctrl + C'.\n\n"
    )
    print(welcome_message)

    print("? 名前を変更したいファイルが含まれるフォルダの絶対パスを入力してください。" if is_japanese else "? Please enter the absolute path of the folder containing the file you wish to rename.")

    while True:
        folder_path = validate_path()
        all_files = count_files(folder_path)
        if all_files <= 0:
            print("\nN 入力されたフォルダにアクセスしましたがファイルが一つも見つかりませんでした。再度フォルダの絶対パスを入力してください。" if is_japanese else "\nN Accessed the entered folder but couldn't find any files. Please enter the absolute path of the folder again.")
            previous_path = None
            continue
        os.chdir(folder_path)
        print(f"\nP {folder_path}\n")

        confirmation_message = (
            (f"? 本当にフォルダ内すべてのファイルの名前を変更してもよろしいですか？\n" if is_japanese else f"? Are you sure you want to rename the files within the folder?\n") +
            (
                (f" 「{os.path.basename(folder_path)}」フォルダ内の{all_files}個のファイルの名前を変更します。一度実行すると元に戻すことはできません。\n" if all_files <= 1 else f" 「{os.path.basename(folder_path)}」フォルダ内の{all_files}個すべてのファイルの名前を変更します。一度実行すると元に戻すことはできません。\n")
                if is_japanese else
                (f"  {all_files} file within the '{os.path.basename(folder_path)}' folder will be renamed. Once executed, this action cannot be undone.\n" if all_files <= 1 else f"  {all_files} files within the '{os.path.basename(folder_path)}' folder will be renamed. Once executed, this action cannot be undone.\n")
            ) +
            ("- 開始するには「Enterキー」を、終了するには右上の閉じるボタンをクリックするか、「Ctrl + C」を押してください。 " if is_japanese else "- To start, press the 'Enter key'. To exit, click the close button in the top right or press 'Ctrl + C'. ")
        )
        print(input(confirmation_message))

        folder_list = [folder_path] + [f for f in glob(os.path.join(folder_path, '*')) if os.path.isdir(f)]

        for folder in folder_list:
            rename_files(folder)
        for error_message in error_messages:
            print(error_message)

        if 0 < renamed_files:
            print(
                f": {all_files}個のファイルを検索して{renamed_files}個のファイルの名前を変更しました。\n" if all_files <= 1 else f": {all_files}個すべてのファイルを検索して{renamed_files}個のファイルの名前を変更しました。\n"
                if is_japanese else
                f": We searched through {all_files} file and renamed {renamed_files} of them.\n" if all_files <= 1 else f": We searched through {all_files} files and renamed {renamed_files} of them.\n"
            )
        else:
            print(": 名前の変更を行うファイルがありませんでした。\n" if is_japanese else ": There were no files to rename.\n")

        choice_message = (
            f"? 再度「{os.path.basename(folder_path)}」フォルダ内のファイルに名前変更をする場合は「Enterキー」を押してください。\n"
             "  また、別のフォルダのファイルに名前変更を行いたい場合はそのファイルが含まれるフォルダの絶対パスを入力してください。"
            if is_japanese else
            f"? If you want to rename files within the '{os.path.basename(folder_path)}' folder again, press the 'Enter key'.\n"
             "  If you want to rename files in a different folder, please input the absolute path to that folder containing the desired files."
        )
        print(choice_message)

        all_files = renamed_files = 0

if __name__ == "__main__":
    is_japanese = language_settings()
    previous_path, renamed_files, error_messages = "", 0, []
    main()
