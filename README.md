## Scripts for processing FACoP/FUNAGE-Pro input/output

These scripts are used for creating the input for the bacterial annotation tool FACoP (http://facop.molgenrug.nl/) and the Gene Set Enrichment tool FUNAGE-Pro (http://funagepro.molgenrug.nl/).

### Preprocessing files for annotation with FACoP

**Important**: Most bacterial genome can be annotated as-is with FACoP as long as the *.gff* and *.fasta* are given and the genome size is below 10 Mbp.

For longer Genomes the *.fasta* and *.gff* files need to be split.
```
usage: FACoP preprocessor [-h] [-o OUTPUT] fasta gff threshold

The FACoP webserver only provides annotations for genomes with a length smaller than 10 Mbp. This tool creates artificial contigs below a specified length threshold that
can be used as input. It preferably splits the file into existing contigs but if a single contig is above the threshold it will be cut between genes.

positional arguments:
  fasta                 fasta file to split
  gff                   gff file to split
  threshold             maximum length of resulting contigs

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output folder
```

### Post-processing files after enrichment with FUNAGE-Pro
Transforms the columns of the FUNAGE-Pro output and saves the result as an *.xlsx* file
```
usage: FUNAGE-Pro postprocessor [-h] [-o OUTPUT] input

Enhances the output table of FUNAGE-Pro and saves it to .xlsx files. Please make sure to export all columns in FUNAGE-Pro

positional arguments:
  input                 folder containing FUNAGE-Pro files

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output folder
```
### Transforming FACoP annotation for usage in GO-Compass
Go-Compass (https://go-compass-tuevis.cs.uni-tuebingen.de/) requires a transformation of the GO Annotation that can be done with this script.
```
usage: FACoP annotation to GO-Compass annotation [-h] input output

Transforms FACoP GO annotation to the annotation format used by GO-Compass

positional arguments:
  input       .tsv or .txt containing GO annotation created by FACoP
  output      Name of output file

options:
  -h, --help  show this help message and exit
```