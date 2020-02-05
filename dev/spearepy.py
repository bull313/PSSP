import os

from speareparser import Parser

SOURCE_CODE_FILENAME = "test/speareparse_test"
PY_EXT = ".spl"
FILE_READ = "r"

def get_input_source(filename):
    source_file = open(filename, FILE_READ)
    return source_file.read()

def main():
    _, _, test_files = next(os.walk("./test"))
    test_file_count = len(test_files)

    for test_num in range(test_file_count):
        print("Test %d... " % test_num)
        source_code = get_input_source("%s%d%s" % (SOURCE_CODE_FILENAME, test_num, PY_EXT))
        parser = Parser(source_code)
        parser.parse()
        print("Success!")

if __name__ == "__main__":
    main()
