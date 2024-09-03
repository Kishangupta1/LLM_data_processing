import pandas as pd
from tqdm import tqdm


# function to merge rows with overlap check
def merge_rows(df_l, rows_to_merge, rows_idx_to_drop_list):
    # Start with the first row in the list
    merged_row = df_l.loc[rows_to_merge[0]]

    # Iterate through the remaining rows and merge them if there's no overlap
    for idx, row in enumerate(rows_to_merge[1:]):
        current_row = df_l.loc[row]
        # Slice to ignore the first two columns (question and context)
        merged_slice = merged_row.iloc[4:]
        current_slice = current_row.iloc[4:]

        # Check for overlap: find columns that are non-NaN in both rows (ignoring the first two columns)
        overlap = (merged_slice.notna() & current_slice.notna()).any()

        # Only merge if there is no overlap
        if not overlap:
            merged_row = merged_row.combine_first(current_row)
            rows_idx_to_drop_list.append(rows_to_merge[idx+1])
        else:
            print(f"Skipping merge with row {row} due to overlap.")

    # Replace the first row with the merged row
    df_l.loc[rows_to_merge[0]] = merged_row


if __name__ == '__main__':
    filepath = "op/map_iter_merged_socio_economic_ques4_15_250_5.xlsx"
    df = pd.read_excel(filepath)
    context_group = df.groupby('Mapping')
    rows_idx_to_drop = []
    for group_name, group_df in tqdm(context_group, desc="Processing"):
        if len(group_df.index) > 1:
            merge_rows(df, group_df.index, rows_idx_to_drop)

    # Drop all other rows in the list
    df.drop(rows_idx_to_drop, inplace=True)

    # Save the updated DataFrame back to an Excel file
    output_path = 'op/map_merged_socio_economic_ques4.xlsx'  # Replace with desired output file path
    df.to_excel(output_path, index=False)
