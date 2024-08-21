import json
import requests
import pandas as pd
from tqdm import tqdm
import config as cfg


# open prompt files
with open(cfg.question_sim) as f:
    msg_data_ques = json.load(f)
    
    
def get_similar_question_idx(idx, question_list):
    # System msg
    msg_list_ques = [json.dumps({"role": "system", "content": msg_data_ques["system"]})]
    aug_msg_hypo = msg_data_ques['history'][0][
                  'user'] + f"{list(zip(idx, question_list))}"
    msg_list_ques.append(json.dumps({"role": "user", "content": aug_msg_hypo}))
    try:
        res_hypo = requests.post(cfg.llm_url + cfg.llm_endpoint, data={'messages': msg_list_ques})
        str_out_hypo = res_hypo.content.decode()
        similar_question_list = json.loads(str_out_hypo.strip())['content']
    except Exception as e:
        similar_question_list = ""
        print(f"can't do with error {e}")
    return similar_question_list


def merge_rows(df, rows_to_merge, rows_idx_to_drop_list):
    # Start with the first row in the list
    merged_row = df.loc[rows_to_merge[0]]

    # Iterate through the remaining rows and merge them
    for row in rows_to_merge[1:]:
        merged_row = merged_row.combine_first(df.loc[row])

    # Replace the first row with the merged row
    df.loc[rows_to_merge[0]] = merged_row

    # Add rows idx to drop
    rows_idx_to_drop_list.extend(rows_to_merge[1:])


if __name__ == '__main__':
    filepath = "op/socio_economic_ques2.xlsx"
    df = pd.read_excel(filepath)
    rows_idx_to_drop = []
    context_group = df.groupby('context')
    for group_name, group_df in tqdm(context_group, desc="Processing"):
        # Access the 'question' column of the group
        similar_question_idx = get_similar_question_idx(group_df.index, group_df['question'])
        similar_question_idx_list = eval(similar_question_idx)
        if isinstance(similar_question_idx_list, list):
            for idx_list in similar_question_idx_list:
                merge_rows(df, idx_list, rows_idx_to_drop)
        else:
            print(f"Can't convert to list: {similar_question_idx}")

    # Drop all other rows in the list
    df.drop(rows_idx_to_drop, inplace=True)

    # Save the updated DataFrame back to an Excel file
    output_path = 'op/merged_socio_economic_ques2.xlsx'  # Replace with desired output file path
    df.to_excel(output_path, index=False)

