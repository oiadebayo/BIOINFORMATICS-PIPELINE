import json
import subprocess
from virulencefinder import run_virulencefinder
from amrgenes import run_amrfinderplus
from plasmidfinder import run_plasmidfinder
from snpanalysis import run_snp_analysis
from genome_annotation import run_genome_annotation


def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)


def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config


def main():
    config = load_config('config.json')
    species = config['species']
    data_dir_prokka = config['data_dir_prokka']
    data_dir_bakta = config['data_dir_bakta']
    tool = config['tool']

    run_virulencefinder(species, data_dir_prokka)
    run_amrfinderplus(species, data_dir_prokka)
    run_plasmidfinder(species)
    reference = "reference.fas"  # Adjust this as needed
    recombination = ""  # Adjust this as needed
    run_snp_analysis(species, reference, recombination)
    data_dir = data_dir_prokka if tool == "prokka" else data_dir_bakta
    run_genome_annotation(species, tool, data_dir)


if __name__ == "__main__":
    main()
