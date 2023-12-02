import pandas as pd
import ast

def pre_processing(path):
    col_names = ["text", "label", "id"]
    df = pd.read_csv(path, sep="\t", names=col_names)
    
    # turn the labels into list
    df["label"] = [labels.split(",") for labels in df["label"]]

    df_filtered = df[df['label'].str.len() > 1]

    # explod the dataframe
    df_exploded = df_filtered.explode('label')

    # change label data type
    df_exploded["label"] = df_exploded["label"].astype("int")
    
    # exclude the neutral emotion
    df_res = df_exploded[df_exploded["label"] != 0]

    df_res["aug_text"] = df_res["text"]

    # df_res = df_res.drop_duplicates(subset='text', keep="first")

    return df_res[["text", "aug_text", "label"]]

train = pre_processing("./full_dataset/train.tsv")
dev = pre_processing("./full_dataset/dev.tsv")
test = pre_processing("./full_dataset/test.tsv")

# train_orig = pd.read_csv("./train.csv")
# val_orig = pd.read_csv("./valid.csv")
# test_orig = pd.read_csv("./test.csv")

# train = pd.concat([train_orig, train.iloc[400:450]])
# dev = pd.concat([val_orig, dev.iloc[400:450]])
# test = pd.concat([test_orig, test.iloc[400:450]])

train.to_csv("./multi-label/train.csv",index=False)
dev.to_csv("./multi-label/valid.csv", index=False)
test.to_csv("./multi-label/test.csv", index=False)

