class LibraryManager:
    FILE_NOT_FOUND_ERROR = "File not found"

    def __init__(self, file_path):
        self.file_path = file_path


    def parse_dependencies(self):
        dependency_dict = {}
        key_dict = []

        try:
            with open(self.file_path, "rb") as file_reader:
                lines = file_reader.read()

            for line in lines.decode().strip().split("\n"):
               if line:
                   key, *value = line.split(" depends on ")
                   if value:
                       dependency_dict[key] = value[0].split(" ")
                   else:
                          dependency_dict[key] = []
                   key_dict.append(key)

            self.arrange_dependencies(dependency_dict, key_dict)
            return self.parse_output(key_dict, dependency_dict)
        except FileNotFoundError:
            return self.FILE_NOT_FOUND_ERROR


    @staticmethod
    def arrange_dependencies(dependency_dict, key_dict):
        for key in key_dict:
            for inner_key, value in dependency_dict.items():
                if key in value:
                    dependency_dict[inner_key].extend(dep for dep in dependency_dict[key] if dep not in value)


    @staticmethod
    def parse_output(key_dict, dependency_dict):
        result = ""
        for key in key_dict:
            result += f"{key} depends on {', '.join(sorted(set(dependency_dict[key])))}\n" if dependency_dict[key] else f"{key}\n"
        return result


if __name__ == "__main__":
    file = input("Enter the file path: ")
    ldm = LibraryManager(file)
    print(ldm.parse_dependencies())