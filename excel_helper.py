from string import ascii_uppercase as upper
from itertools import chain, product
import pandas as pd, numpy as np

excel_labels = list(map(lambda l: ''.join(l),chain(upper, product(upper, repeat=2))))[:100]

def xlsx_exporter(sheets, file_name):
    """Pandas df to xlsx
    Supply dict of sheets: sheets = { 'sheet_name' : df }
    """
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter', options={'strings_to_urls': False})

    for sheet in sheets:
        print(f'Loading {sheet}')
        xlsx_df = sheets[sheet]
    
        xlsx_df.to_excel(writer, sheet_name=sheet, index=False, freeze_panes=(1,0))  # send xlsx_df to writer
        worksheet = writer.sheets[sheet]  # pull worksheet object
        filter_range = f"A1:{excel_labels[len(xlsx_df.columns) - 1]}{len(xlsx_df.index) + 1}"
        worksheet.autofilter(filter_range)
    
        for idx, col in enumerate(xlsx_df):  # loop through all columns
            series = xlsx_df[col]
            max_len = max((series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name)) )) + 1  # len of column name/header with added padding
            max_len = 50 if max_len > 50 else max_len
            worksheet.set_column(idx, idx, max_len + 2)
            
    print('\nSaving Excel file...')
    writer.save()
    writer.close()