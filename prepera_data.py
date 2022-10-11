import pandas as pd
from get_data_from_server import create_folder
from time import time

def get_data() -> pd.DataFrame:
    data = pd.read_csv('products.csv', sep=',', encoding='utf-8', index_col=None)
    try:
        data = data.drop(['Remarks','PromotionalPrice', 'LineNumber', 'LineType', 'Size', 'UnitOfMeasure', 'ReferenceNumber'], axis=1)
    except KeyError:
        pass
    return data

def norm_EAN(data) -> pd.DataFrame:
    data['EAN'] = data['EAN'].fillna(0).astype(int)
    for i in data['EAN']:
        if len(str(i)) > 13:
            data.loc[data['EAN'] == i, 'EAN' ] = str(i)[:13]
    return data

def norm_FUN(data) -> pd.DataFrame:
    list_to_del = ['®', '™', '"', ';']
    for val in list_to_del:
        data['FunctionalName'] = data['FunctionalName'].str.replace(val,'')
    # for line in data['FunctionalName']:
    #     for item in list_to_del:
    #         data.loc[data['FunctionalName'] == line, 'FunctionalName' ] = line.replace(item, '')
    return data

def remove_replaced(data) -> pd.DataFrame:
    data = data.drop_duplicates('EAN')
    data = data.reset_index(drop=True)
    return data
    # new_data = pd.DataFrame(columns=list(data), index=None)
    # for row in range(1, len(data.index)):
    #     if not data['EAN'].loc[row-1] == data['EAN'].loc[row]:
    #         new_data.loc[len(new_data)] = data.loc[row]
    # return new_data

def norm_Cat(data) -> pd.DataFrame:
    cat_norm = []
    pd.Series(data['CategoryPath'], index=None).to_csv('Kategorie.csv', index=None, sep=';', encoding='utf-8')
    for vale in data['CategoryPath']:
        vale = vale.replace(r'/', '-')
        # value = vale.split('::')
        # if value[2] == '':
        #     cat_norm.append(f'{value[0]};{value[1]}')
        # else:    
        #     cat_norm.append(f'{value[0]};{value[1]};{value[2]}')
        
        if vale[-2:] == '::':
            vale = vale[:-2]
        cal = vale.split('::')[::-1]
        cal.append('Strona główna')
        cat_norm.append(';'.join(cal))
    data['Cat'] = cat_norm
    return data

def data_to_csv(data):
    data.to_csv('products_after_prepere.csv', sep=',', encoding='utf-8', index=None)

def norm_tax(data:pd.DataFrame):
    tax_norm = []
    for vale in data['TaxRate']:
        match (vale):
            case 23:
                tax_norm.append(1)
            case 8:
                tax_norm.append(2)
            case 5:
                tax_norm.append(3)
            case 0:
                tax_norm.append(4)
    data['Tax'] = tax_norm
    data = data.drop('TaxRate', axis=1).reset_index(drop=True)
    return data

if __name__ == '__main__':
    t = time()
    create_folder()
    data = get_data()
    print(f'Ilość produktów przed normalizacją: {len(data.index)}')
    data = norm_EAN(data)
    data = norm_FUN(data)
    data = remove_replaced(data)
    data = norm_tax(data)
    data = norm_Cat(data)
    print(f'Ilość produktów po normalizacji: {len(data.index)}')
    data_to_csv(data)
    print(f'Czas: {time() - t}')
