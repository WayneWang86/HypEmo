import subprocess
import pandas as pd
from sklearn.metrics import f1_score, recall_score, precision_score
import argparse

idx2label = {0: 'admiration', 1: 'amusement', 2: 'anger', 3: 'annoyance', 4: 'approval', 
            5: 'caring', 6: 'confusion', 7: 'curiosity', 8: 'desire', 9: 'disappointment', 10: 'disapproval', 
            11: 'disgust', 12: 'embarrassment', 13: 'excitement', 14: 'fear', 15: 'gratitude', 16: 'grief', 
            17: 'joy', 18: 'love', 19: 'nervousness', 20: 'optimism', 21: 'pride', 22: 'realization', 
            23: 'relief', 24: 'remorse', 25: 'sadness', 26: 'surprise'}

label2group = {'amusement': 'positive', 'excitement': 'positive', 'joy': 'positive', 'love': 'positive', 'desire': 'positive', 
                'optimism': 'positive', 'caring': 'positive', 'pride': 'positive', 'admiration': 'positive', 'gratitude': 'positive', 
                'relief': 'positive', 'approval': 'positive', 'fear': 'negative', 'nervousness': 'negative', 'remorse': 'negative', 
                'embarrassment': 'negative', 'disappointment': 'negative', 'sadness': 'negative', 'grief': 'negative', 'disgust': 'negative', 
                'anger': 'negative', 'annoyance': 'negative', 'disapproval': 'negative', 'realization': 'ambiguous', 
                'surprise': 'ambiguous', 'curiosity': 'ambiguous', 'confusion': 'ambiguous'}

label2senti = {'anger': 'anger', 'annoyance': 'anger', 'disapproval': 'anger', 'disgust': 'disgust', 'fear': 'fear', 'nervousness': 'fear', 
                'joy': 'joy', 'amusement': 'joy', 'approval': 'joy', 'excitement': 'joy', 'gratitude': 'joy', 'love': 'joy', 'optimism': 'joy', 'relief': 'joy', 
                'pride': 'joy', 'admiration': 'joy', 'desire': 'joy', 'caring': 'joy', 'sadness': 'sadness', 'disappointment': 'sadness', 'embarrassment': 'sadness',
                'grief': 'sadness', 'remorse': 'sadness', 'surprise': 'surprise', 'realization': 'surprise', 'confusion': 'surprise', 'curiosity': 'surprise'}

senti2label = {
                "anger": ["anger", "annoyance", "disapproval"],
                "disgust": ["disgust"],
                "fear": ["fear", "nervousness"],
                "joy": ["joy", "amusement", "approval", "excitement", "gratitude",  "love", "optimism", "relief", "pride", "admiration", "desire", "caring"],
                "sadness": ["sadness", "disappointment", "embarrassment", "grief",  "remorse"],
                "surprise": ["surprise", "realization", "confusion", "curiosity"]
            }

label2idx = {'admiration': 0, 'amusement': 1, 'anger': 2,
      'annoyance': 3, 'approval': 4, 'caring': 5,
      'confusion': 6, 'curiosity': 7, 'desire': 8,
      'disappointment': 9, 'disapproval': 10, 'disgust': 11,
      'embarrassment': 12, 'excitement': 13, 'fear': 14,
      'gratitude': 15, 'grief': 16, 'joy': 17,
      'love': 18, 'nervousness': 19, 'optimism': 20,
      'pride': 21, 'realization': 22, 'relief': 23,
      'remorse': 24, 'sadness': 25, 'surprise': 26}

group2label = {
                "positive": ["amusement", "excitement", "joy", "love", "desire", "optimism", "caring", "pride", "admiration", "gratitude", "relief", "approval"],
                "negative": ["fear", "nervousness", "remorse", "embarrassment", "disappointment", "sadness", "grief", "disgust", "anger", "annoyance", "disapproval"],
                "ambiguous": ["realization", "surprise", "curiosity", "confusion"]
            }

def run_training_script():
    # Run the training script
    subprocess.run(["python", "train.py"], check=True)

def error_analysis(df):
    # Define your error analysis function
    # This function should take a DataFrame as input and perform the analysis
    pass

def generate_evaluation(labels, true_col, pred_col):
    f1_scores = []
    recall_scores = []
    precision_scores = []
    
    for label in labels:
        true_labels = (output[true_col] == label).astype(int)
        predicted_labels = (output[pred_col] == label).astype(int)

        f1 = f1_score(true_labels, predicted_labels)
        recall = recall_score(true_labels, predicted_labels)
        precision = precision_score(true_labels, predicted_labels)

        f1_scores.append(f1)
        recall_scores.append(recall)
        precision_scores.append(precision)
    result_df = pd.DataFrame({'Label': labels, 'F1_Score': f1_scores, 'Recall': recall_scores, 'Precision': precision_scores})
    return result_df

def set_environment_variable(methods):
    os.environ['METHOD'] = methods
    print(f"Environment variable 'METHOD' set to: {methods}")


def main(methods):
    # Run the training script
    run_training_script()
    output = pd.read_csv('output.csv')
    output.to_csv(f'output_{methods}.csv')
    # # Read the output CSV file
    # # Replace 'output.csv' with the actual name of the CSV file generated by train.py
    true_label = pd.read_csv('data/go_emotion/test.csv')
    output = pd.concat([test_data[['text', 'aug_text', 'label']], output], axis=1)

    # Reset the index if needed
    output.reset_index(drop=True, inplace=True)

    ## emotion id to fine-grained label
    fine_grained_labels = label2idx.keys()
    output['predict_label'] = output['Predicted_Label'].replace(idx2label)
    output['true_label'] = output['label'].replace(idx2label)
    fine_grained_res = generate_evaluation(fine_grained_labels, 'true_label', 'predict_label')

    ## Analyze Using Ekman's Grouping Method
    Ekman_labels = label2senti.keys()
    output['predict_senti'] = output['predict_label'].replace(label2senti)
    output['true_senti'] = output['true_label'].replace(label2senti)
    Ekman_res = generate_evaluation(Ekman_labels, 'true_senti', 'predict_senti')
    
    ## Analyze Using Sentiment Taxomony Method
    Taxomony_labels = group2label.keys()
    output['predict_group'] = output['predict_label'].replace(label2group)
    output['true_group'] = output['true_label'].replace(label2group)
    Taxomony_res = generate_evaluation(Ekman_labels, 'true_group', 'predict_group')

    ## Save all the result into  a csv file
    empty_row = pd.DataFrame({col: [''] for col in fine_grained_res.columns})
    # Concatenate all DataFrames with an empty row in between
    combined_df = pd.concat([fine_grained_res, empty_row, Ekman_res, empty_row, Taxomony_res], ignore_index=True)

    # Write the combined DataFrame to a CSV file
    combined_df.to_csv(f'error_analysis_results_{methods}.csv', index=False)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Script that processes methods")
    parser.add_argument('--methods', nargs='+', help='List of methods to process')
    args = parser.parse_args()

    set_environment_variable(args.methods)
    
    main(args.methods)