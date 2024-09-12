import json
import requests
import pandas as pd
from tqdm import tqdm
import config as cfg
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import copy

sim_threshold = 0.6


# open prompt files
with open(cfg.get_topic) as f:
    msg_data_clus = json.load(f)


def get_topic(rows_list):
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


def transform_data(series):
    def process_element(element):
        map_idx = []
        if isinstance(element, str):
            for item in re.split(r'[,\n]', element):
                item = item.strip()
                key1 = next((k for k, v in idx_topic.items() if item in v[1]), None)
                map_idx.append(key1)
        else:
            item = str(element)
            key2 = next((k for k, v in idx_topic.items() if item in v[1]), None)
            map_idx.append(key2)
        return map_idx

    # Apply the process_element function to each element in the series
    return series.apply(process_element)


if __name__ == '__main__':
    filepath = "op/ques_map_merged_socio_economic_ques.xlsx"
    df = pd.read_excel(filepath)
    start_col = 3
    end_col = 20
    # for i in tqdm(range(len(df)), desc="Processing"):
    #     ###############DEBUG#####################
    #     if i == 18:
    #         break
        ############################
    idx = 16
    row = df.iloc[idx, start_col:]
    # row_series = df.loc[idx, df.columns[start_col:]][df.loc[idx, df.columns[start_col:]].notna()]
    # res = []
    row_unique_series = row.drop_duplicates()
    split_list = sum(row_unique_series.apply(
        lambda text: [item.strip() for item in re.split(r'[,\n]', text)] if isinstance(text, str) else [str(text)]), [])

    all_variables_unique = set(split_list)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sent_list = list(all_variables_unique)
    embeddings = model.encode(list(sent_list))
    cosine_sim_matrix = cosine_similarity(embeddings)
    # for _ in range(10):
    sentence_dict = {}
    visited = set()
    # keep similar sents in a dict
    for i in tqdm(range(len(sent_list))):
        if i in visited:
            continue
        similar_sentences = [sent_list[i]]
        visited.add(i)
        for j in range(len(sent_list)):
            if i != j and cosine_sim_matrix[i, j] >= sim_threshold:
                similar_sentences.append(sent_list[j])
                visited.add(j)
        # Use the first sentence as the key for the group
        sentence_dict[sent_list[i]] = similar_sentences
        # sim_threshold += .1
        # with open(f'similar_sent_{sim_threshold}.json', 'w') as f:
        #     json.dump(sentence_dict, f)
    idx_topic = {}  # map topic to idx/int
    for pos, (key, val) in enumerate((copy.deepcopy(sentence_dict)).items()):
        topic = get_topic(val)
        sentence_dict[topic] = sentence_dict.pop(key)
        idx_topic[pos] = (topic, val)

    # df.iloc[idx, start_col:] = df.iloc[idx, start_col:].apply(transform_data)
    df.iloc[idx, start_col:] = transform_data(df.iloc[idx, start_col:])
    print('here')

    # clustered_row = get_clustered_row(row_unique_series[start_col:end_col])
    # while not row_unique_series.empty:
    #     clustered_row = get_clustered_row(row_unique_series[:10])
    #     row_unique_series = row_unique_series[10:]
    #     # res.append(clustered_row)
    #     with open("llm_res.txt", "a") as f:
    #         f.write(clustered_row)
    # df.iloc[idx] = clustered_row


    # Save the updated DataFrame back to an Excel file
    # output_path = 'op/clustered_socio_economic_ans.xlsx'  # Replace with desired output file path
    # df.to_excel(output_path, index=False)
