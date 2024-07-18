import os
from datetime import datetime
from main import run_command


def run_snp_analysis(species, reference, recombination):
    session_name = "snp_phylogeny_session"
    date_str = datetime.now().strftime('%Y-%m-%d')
    data_dir = "/data/home/ife_akintayo/projects/2020-02-18"
    input_dir = os.path.join(data_dir, "species_fastqs", species)
    output_dir = os.path.join(data_dir, "snp_phylogeny_output", species, date_str)
    scripts_dir = os.path.join(output_dir, "scripts")
    script_path = os.path.join(scripts_dir, "run_snp_phylogeny_pipeline.sh")
    source_script = "/data/ghru/scripts/run_snp_phylogeny_pipeline.sh"

    os.makedirs(scripts_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    run_command(f"tmux new -d -s {session_name}")
    run_command(f"cp {source_script} {script_path}")
    run_command(f"sed -i 's/<SPECIES>/{species}/' {script_path}")
    run_command(f"sed -i 's|<REFERENCE>|{reference}|' {script_path}")
    run_command(f"sed -i 's|<RECOMBINATION>|{recombination}|' {script_path}")
    run_command(f"sed -i 's|<DATA_DIR>|{data_dir}|' {script_path}")
    run_command(f"sed -i 's|<INPUT_DIR>|{input_dir}|' {script_path}")
    run_command(f"sed -i 's|<DATE>|{date_str}|' {script_path}")
    run_command(f"tmux send-keys -t {session_name} 'bash {script_path}' C-m")
    print("SNP Analysis step completed.")
