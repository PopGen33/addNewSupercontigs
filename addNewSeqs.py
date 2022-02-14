
# Script requires Python 3 and Biopython

from Bio import SeqIO
import re, os

def newOutputFasta(rec, oldSupercontig, pathToSC, outDir, addNew):
    supercontigFile = pathToSC + oldSupercontig + "_supercontig.fasta"
    if os.path.exists(supercontigFile):
        with open(supercontigFile, "r") as old:
            oldContigs = SeqIO.parse(old, "fasta")
            with open(outDir + oldSupercontig + "_supercontig.fasta", "w") as out:
                SeqIO.write(oldContigs, out, "fasta")
                SeqIO.write(rec, out, "fasta")
    else:
        if addNew:
            print("Old supercontigs for " + oldSupercontig + " not found! Creating new file.")
            with open(outDir + oldSupercontig + "_supercontig.fasta", "w") as out:
                SeqIO.write(rec, out, "fasta")
        else:
            print("Old supercontigs for " + oldSupercontig + " not found! Skipping locus.\n")

def main():
    ### ALL important variables are set here ###
    pathToNewSeqs = "./NewSpeciesLoci.fasta" # Path to fasta file with new sequences
    pathToSupercontigs = "./ExampleSupercontigs/" # Path to directory with fasta files filled with supercontigs (must end in /)
    pathToOutDir = "./ExampleSupercontigs_output/" # Output directory (must end in /)
    addNewLoci = True # toggle whether new loci not previously in the supercontigs folder but present in the new sequences file get added
    
    print("Adding new sequences to supercontigs...\n")
    
    if not os.path.exists(pathToOutDir):
        os.makedirs(pathToOutDir)
    
    with open(pathToNewSeqs,"r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            # extract identifier for supercontig file from record.id
            pattern = re.compile(r'_([0-9]+)')
            supercontig = re.search(pattern, record.id).group(1)
            newOutputFasta(record, supercontig, pathToSupercontigs, pathToOutDir, addNewLoci)
            print("Added " + record.id + " to " + supercontig + "\n")
    print("Done! All output in " + pathToOutDir)

if __name__ == "__main__":
	main()