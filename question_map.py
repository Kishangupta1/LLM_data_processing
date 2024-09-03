import pandas as pd
from tqdm import tqdm


def get_key_for_value_in_list(d, search_value):
    for key, value_list in d.items():
        if any(search_value == value for value in value_list):
            return key
    return None


if __name__ == '__main__':
    filepath = r"C:\Users\Kishan Gupta\Downloads\map_iter_merged_socio_economic_ques4_15_250_5.xlsx"
    df = pd.read_excel(filepath)
    map_dict = {}
    for idx in range(len(df)):
        if df['Mapping'][idx] not in map_dict:
            map_dict[df['Mapping'][idx]] = [df['question'][idx]]
        else:
            map_dict[df['Mapping'][idx]].append(df['question'][idx])

    df2 = pd.read_excel("op/iter_merged_socio_economic_ques.xlsx")
    column_dict = {"question": [], "mapping": []}
    for idx in range(len(df2)):
        key = get_key_for_value_in_list(map_dict, df2['question'][idx])
        # key = map_dict.get(df2['question'][idx], None)
        column_dict["question"].append(df2['question'][idx])
        column_dict["mapping"].append(key)

    # new df
    df3 = pd.DataFrame()
    for col_name, col_values in column_dict.items():
        df3[col_name] = col_values

    # Save the updated DataFrame back to an Excel file
    output_path = 'op/map_ques.xlsx'  # Replace with desired output file path
    df3.to_excel(output_path, index=False)
