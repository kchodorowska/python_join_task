import sys
import pandas
import os


def join(a, b, c, d):
    return a.merge(b, on=[c], how=d)


def change_type(file, col):
    max_value = file[col].max()
    min_value = file[col].min()
    if max_value < 128 and min_value > -129:
        file[col] = file[col].astype("int8")
    if max_value < 32768 and min_value > -32769:
        file[col] = file[col].astype("int16")


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Number of arguments is not in a range!")
        exit()

    if not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2]):
        print("File path does not exist!")
        exit()

    csv_file1_path = pandas.read_csv(sys.argv[1])

    csv_file2_path = pandas.read_csv(sys.argv[2])

    for column in csv_file1_path:
        if pandas.api.types.is_integer_dtype(csv_file1_path[column].dtype):
            change_type(csv_file1_path, column)

    for column in csv_file2_path:
        if pandas.api.types.is_integer_dtype(csv_file2_path[column].dtype):
            change_type(csv_file2_path, column)

    col_name = sys.argv[3]

    if not csv_file1_path.columns.__contains__(col_name) or not csv_file2_path.columns.__contains__(col_name):
        print("There is no such column!")
        exit()

    join_types = ['inner', 'left', 'right']

    if len(sys.argv) == 4:
        join_type = 'inner'
    else:
        if sys.argv[4] in join_types:
            join_type = sys.argv[4]
        else:
            print("There is no such join type!")
            exit()

    print(join(csv_file1_path, csv_file2_path, col_name, join_type))
