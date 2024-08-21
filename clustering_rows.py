import json
import requests
import pandas as pd
from tqdm import tqdm
import config as cfg


# open prompt files
with open(cfg.clustering_rows) as f:
    msg_data_clus = json.load(f)


def get_clustered_row(rows_list):
    # System msg
    msg_list_clus = [json.dumps({"role": "system", "content": msg_data_clus["system"]})]
    aug_msg_hypo = msg_data_clus['history'][0][
                  'user'] + f"{rows_list}"
    msg_list_clus.append(json.dumps({"role": "user", "content": aug_msg_hypo}))
    try:
        res_hypo = requests.post(cfg.llm_url + cfg.llm_endpoint, data={'messages': msg_list_clus})
        str_out_hypo = res_hypo.content.decode()
        cluster = json.loads(str_out_hypo.strip())['content']
    except Exception as e:
        cluster = ""
        print(f"can't do with error {e}")
    return cluster


if __name__ == '__main__':
    filepath = "op/merged_socio_economic_ques2.xlsx"
    df = pd.read_excel(filepath)
    start_col = 3
    for i in tqdm(range(len(df)), desc="Processing"):
        ###############DEBUG#####################
        if i == 18:
            break
        ############################
        row = df.iloc[i, start_col:40].to_list()
        clustered_row = get_clustered_row(row)
        df.iloc[i] = clustered_row

    # Save the updated DataFrame back to an Excel file
    output_path = 'op/clustered_socio_economic_ans.xlsx'  # Replace with desired output file path
    df.to_excel(output_path, index=False)
