import pandas as pd
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="python facop_to_gocompass.py",
                                     description="Transforms FACoP GO annotation to the annotation format used by GO-Compass")
    parser.add_argument("input", help=".tsv or .txt containing GO annotation created by FACoP")
    parser.add_argument("output", help="Name of output file")

    args = parser.parse_args()


    # Read the TSV data into a DataFrame
    df = pd.read_csv(args.input, sep='\t')

    # Group by 'locus_tag' and aggregate the 'class' values into a semicolon-separated string
    df_result = df.groupby('locus_tag')['class'].agg(lambda x: ';'.join(x)).reset_index()

    # Display the resulting DataFrame
    df_result.to_csv(args.output,sep="\t",index=False,header=False)
