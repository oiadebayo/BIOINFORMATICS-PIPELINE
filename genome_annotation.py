import os
from main import run_command


def run_genome_annotation(species, tool, data_dir):
    session_name = f"{tool}_session"
    output_dir = os.path.join(data_dir, f"{tool}_output", species, "scripts")
    script_path = os.path.join(output_dir, f"run_{tool}_for_multiple.sh")
    source_script_prokka = "/data/ghru/scripts/run_prokka_for_multiple.sh"
    source_script_bakta = "/data/ghru/scripts/run_bakta.sh"
    source_script = source_script_prokka if tool == "prokka" else source_script_bakta

    os.makedirs(output_dir, exist_ok=True)
    run_command(f"tmux new -d -s {session_name}")
    run_command(f"cp {source_script} {script_path}")
    run_command(f"sed -i 's/<SPECIES>/{species}/' {script_path}")
    run_command(f"sed -i 's|<DATA_DIR>|{data_dir}|' {script_path}")

    if tool == "bakta":
        run_command(f"tmux send-keys -t {session_name} 'conda activate bakta' C-m")

    run_command(f"tmux send-keys -t {session_name} 'bash {script_path}' C-m")

    if tool == "bakta":
        run_command(f"tmux send-keys -t {session_name} 'conda deactivate' C-m")

    print(f"{tool.capitalize()} step completed.")
