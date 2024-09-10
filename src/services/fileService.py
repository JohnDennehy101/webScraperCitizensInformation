import os
import urllib.parse
import re

class FileService:
    # Initiate with directory where to store files
    # in constructor, create directory if it does not exist

    # Method to write to file with provided file name
    def __init__(self, files_directory):
        self.files_directory = files_directory
        os.makedirs(files_directory, exist_ok=True)
    
    # Method to read from file with provided file name
    def read_from_file(self, file_name):
        file_opened = False
        try:
            relative_file_path = os.path.join(self.files_directory, file_name)

            file = open(f"../{relative_file_path}", "r")
            file_opened = True
            file_contents = file.read()
            return file_contents
        except FileNotFoundError:
            print("The file was not found")
        except ValueError:
            print("It was not possible to open the file")
        finally:
            if file_opened:
                file.close()
    
    # Method to write to file with provided file name and provided content
    def write_to_file(self, new_file_name, new_file_contents):
        file_opened = False
        try:
            relative_file_path = os.path.join(self.files_directory, new_file_name)
            file = open(f"../{relative_file_path}", "w", encoding="utf-8")
            file_opened = True
            file.write(new_file_contents)
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except ValueError:
            print("It was not possible to open the file")
            return False
        except IOError as e:
            print(f"An I/O error occurred: {e}")
            return False
        finally:
            if file_opened:
                file.close()


    # Method to check if file name exists
    def check_file_existence(self, file_name):
        file_path = os.path.join(self.files_directory, file_name)

        if os.path.isfile(f"../{file_path}"):
            return True

        return False


    # Method to sanitise file name
    def sanitise_file_name(self, name):
        parsed_url = urllib.parse.urlparse(name)

        web_domain = parsed_url.netloc.replace("www.", "")
        url_path = parsed_url.path.strip('/').replace("/", "_")

        query_params = parsed_url.query

        if query_params:
            query_params = f"_{query_params.replace('&', '_').replace('=', '_')}"
        else:
            query_params = ""

        if url_path:
            if not url_path.endswith(".html"):
                page_name = f"{web_domain}_{query_params}{url_path}.html"
            else:
                page_name = f"{web_domain}_{query_params}{url_path}"
        else:
            page_name = f"{web_domain}.html"

        page_name = re.sub(r'[^\w\-_\.]', '_', page_name)

        page_name = page_name.lstrip("_")

        return page_name

