from Bio import SeqIO
import os
import argparse


def find_closest_non_gene(gff_data, record_id, split_position):
    for feature in gff_data:
        if feature[0] != record_id or feature[1] != "region":
            continue  # Skip features not related to the current record

        start = int(feature[3]) - 1  # Adjust to 0-based index
        end = int(feature[4])

        if start <= split_position < end:
            # The split position is within a gene, find the closest non-gene position
            if split_position - start < end - split_position:
                return start - 1  # One position before the gene
            else:
                return end  # One position after the gene

    return split_position  # The split position is not within any gene


def split_fasta(records, gff_data, output_folder, length_threshold):
    for record in records:
        if len(record.seq) < length_threshold:
            output_file = f"{output_folder}/{record.id}.fasta"
            SeqIO.write([record], output_file, "fasta")
            print(f"Record '{record.id}' (length: {len(record.seq)}) written to '{output_file}'.")
            output_file_gff = f"{output_folder}/{record.id}.gff"
            with open(output_file_gff, 'a') as new_gff:
                new_gff.write(('\t'.join(feature) for feature in gff_data if feature[0] == record.id) + "\n")
        else:
            # Calculate number of chunks required
            num_chunks = (len(record.seq) + length_threshold - 1) // length_threshold
            print(f"Record '{record.id}' (length: {len(record.seq)}) exceeds the threshold.")
            print(f"It would be split into {num_chunks} chunks to be below the threshold.")

            # Create new records with splits
            for i in range(num_chunks):
                start_pos = i * length_threshold
                end_pos = min((i + 1) * length_threshold, len(record.seq))

                # Find closest non-gene position for split
                adjusted_start_pos = find_closest_non_gene(gff_data, record.id, start_pos)
                adjusted_end_pos = find_closest_non_gene(gff_data, record.id, end_pos)

                new_record_id = f"{record.id}_{i + 1}"
                new_record = record[adjusted_start_pos:adjusted_end_pos]
                new_record.id = new_record_id
                new_record.description = ''
                output_file = f"{output_folder}/{new_record_id}.fasta"
                output_file_gff = f"{output_folder}/{new_record_id}.gff"
                SeqIO.write([new_record], output_file, "fasta")
                print(f"New record '{new_record_id}' (length: {len(new_record.seq)}) written to '{output_file}'.")

                # Adjust GFF coordinates for the new record
                for feature in gff_data:
                    if feature[0] == record.id and int(feature[3]) > adjusted_start_pos and int(
                            feature[4]) < adjusted_end_pos:
                        feature[0] = new_record_id  # Adjust record name
                        feature[3] = str(int(feature[3]) - adjusted_start_pos)  # Adjust start position
                        feature[4] = str(int(feature[4]) - adjusted_start_pos)  # Adjust end position
                        with open(output_file_gff, 'a') as new_gff:
                            new_gff.write(
                                '\t'.join(feature) + "\n")


def parse_gff(gff_file):
    with open(gff_file) as file:
        return [line.strip().split("\t") for line in file if not line.startswith("#")]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="python facop_preprocessing.py",
                                     description="The FACoP webserver only provides annotations for genomes with a length smaller than 10 Mbp. This tool creates artificial contigs below a specified length threshold that can be used as input. It preferably splits the file into existing contigs but if a single contig is above the threshold it will be cut between genes.")
    parser.add_argument("fasta", help="fasta file to split")
    parser.add_argument("gff", help="gff file to split")
    parser.add_argument("threshold", help="maximum length of resulting contigs")
    parser.add_argument("-o", "--output",default="split_output", help="output folder")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    gff_data = parse_gff(args.gff)
    records = list(SeqIO.parse(args.fasta, "fasta"))
    split_fasta(records, gff_data, args.output, int(args.threshold))
