import pandas as pd

EXCEL_EXTENSIONS = set(['xlsx', 'xls'])
CSV_EXTENSIONS = set(['csv'])
ALLOWED_EXTENSIONS = EXCEL_EXTENSIONS | CSV_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_as_dataframe(filename):
    file_path = '/tmp/%s' % (filename)
    extension = filename.rsplit('.', 1)[1].lower()

    if extension in EXCEL_EXTENSIONS:
        return pd.read_excel(file_path)
    elif extension in CSV_EXTENSIONS:
        return pd.read_csv(file_path)

def markdown_table_generator(filename):
    def table_row(list):
        str_list = [str(i) for i in list]
        return '| ' + ' | '.join(str_list) + ' |'

    dataframe = read_as_dataframe(filename)

    table = []
    table.append(table_row(dataframe.columns))
    table.append(table_row( \
        ['--' for i in range(len(dataframe.columns))]))
    for i, row in dataframe.iterrows():
        table.append(table_row(row.values.tolist()))

    return table

