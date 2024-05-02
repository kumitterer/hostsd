from pathlib import Path
from os import PathLike
from typing import Union
from argparse import ArgumentParser
from pathlib import Path

import sys

HOSTS_DIR = "/etc/hosts.d/"
HOSTS_FILE = "/etc/hosts"

HOSTS_DIR_WINDOWS = "C:\\Windows\\System32\\drivers\\etc\\hosts.d\\"
HOSTS_FILE_WINDOWS = "C:\\Windows\\System32\\drivers\\etc\\hosts"


def get_new_content(dirpath: Union[str, PathLike] = HOSTS_DIR) -> str:
    """Read all files from a directory and join their contents in a string

    This will not read files with names that begin with a period ("."), or binary files.

    Args:
        dir (str, optional): The directory from which to read files. Defaults to "/etc/hosts.d/".

    Raises:
        IOError: Raised if the provided source path does not exist or is not a directory.

    Returns:
        str: Joined content of read files
    """
    content: str = ""

    directory = Path(dirpath)

    if not (directory.exists() and directory.is_dir()):
        raise IOError(f"Directory {dirpath} does not exist or is not a directory.")

    for infile in sorted(list(directory.iterdir()), key=lambda f: f.name):
        if (
            infile.is_file()
            and not infile.name.startswith(".")
            and not infile.name.endswith(".disabled")
        ):
            with infile.open('r') as openfile:
                try:
                    filecontent = openfile.read()
                except UnicodeDecodeError:
                    print(f"File {infile.name} is not a text file - skipping")

                if content:
                    content += "\n\n"

                content += f"# {infile.name}\n\n{filecontent}"

    return content


def write_hosts_file(content: str, path: Union[str, PathLike] = HOSTS_FILE):
    """Simple function writing text content to a file given by path

    Args:
        content (str): Text content to be written.
        path (Union[str, PathLike], optional): Path of the file to write to. Defaults to "/etc/hosts".

    Raises:
        IOError: Raised if the provided file path could not be written to.
    """
    with Path(path).open('w') as hostsfile:
        try:
            hostsfile.write(content)
        except Exception as e:
            raise IOError(f"Unable to write file {path} – {e}")


def main():
    parser = ArgumentParser(
        description="Update /etc/hosts file with contents of /etc/hosts.d/ directory"
    )

    parser.add_argument(
        "-d",
        "--dir",
        help=f"Directory containing the hosts files to be merged (default: {HOSTS_DIR})",
        default=HOSTS_DIR,
    )

    parser.add_argument(
        "-o",
        "--output",
        help=f"File to write the merged content to (default: {HOSTS_FILE})",
        default=HOSTS_FILE,
    )

    args = parser.parse_args()

    if args.dir:
        input_dir = Path(args.dir)
    else:
        if sys.platform == "win32":
            input_dir = Path(HOSTS_DIR_WINDOWS)
        else:
            input_dir = Path(HOSTS_DIR)

    if not input_dir.exists():
        print(f"Directory {args.dir} does not exist – exiting")
        return

    if args.output:
        output_file = Path(args.output)
    else:
        if sys.platform == "win32":
            output_file = Path(HOSTS_FILE_WINDOWS)
        else:
            output_file = Path(HOSTS_FILE)

    if not output_file.exists():
        print(f"File {args.output} does not exist – exiting")
        return

    try:
        write_hosts_file(get_new_content(args.dir), args.output)
    except IOError as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
