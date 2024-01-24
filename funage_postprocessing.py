import sys
import os
import argparse
import pandas as pd


def read_file(tsv_file_path, output_file_path):
    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_file_path, sep='\t')

    # Split the values in the "single_list" column by semicolon and create new columns
    df_expanded = df['single_list'].str.split(';', expand=True)

    # Concatenate the new columns to the original DataFrame
    df_result = pd.concat([df, df_expanded], axis=1)

    # Display the resulting DataFrame
    df_result = df_result.drop(columns=["single_list"])
    df_result = df_result.rename(
        columns={"ClassID": "ID", "Class": "Annotation Database",0:"Importance", 1: "Proportion", 2: "p-value", 3: "Genes"})
    df_result["p-value"]=pd.to_numeric(df_result["p-value"])
    df_result["Importance"]=pd.to_numeric(df_result["Importance"])
    df_result=df_result.sort_values(['Annotation Database', 'p-value'], ascending=[True, True])

    df_result.to_excel(output_file_path+".xlsx", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="FUNAGE-Pro postprocessor",
                                     description="Enhances the output table of FUNAGE-Pro and saves it to .xlsx files. Please make sure to export all columns in FUNAGE-Pro")
    parser.add_argument("input", help="folder containing FUNAGE-Pro files")
    parser.add_argument("-o", "--output", default="pretty_output", help="output folder")
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    for filename in os.listdir(args.input):
        if filename.endswith('.txt'):
            # Construct the file paths
            input_file_path = os.path.join(args.input, filename)
            output_file_path = os.path.join(args.output, filename)
            read_file(input_file_path, output_file_path)
