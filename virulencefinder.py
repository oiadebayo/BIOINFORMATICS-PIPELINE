import os
from main import run_command


def run_virulencefinder(species, data_dir):
    session_name = "virulencefinder_session"
    virulence_db = "/data/ghru/databases/vfdb_core/"
    input_dir = os.path.join(data_dir, "species_fastqs", species)
    scripts_dir = os.path.join(data_dir, "scripts", species)
    script_path = os.path.join(scripts_dir, "run_virulencefinder_for_multiple.sh")
    source_script = "/data/ghru/scripts/run_virulencefinder_for_multiple.sh"

    os.makedirs(scripts_dir, exist_ok=True)
    run_command("cd /data/ghru/databases/virulencefinder_db && git pull")
    run_command(f"tmux new -d -s {session_name}")
    run_command(f"cp {source_script} {script_path}")
    run_command(f"sed -i 's/<SPECIES>/{species}/' {script_path}")
    run_command(f"sed -i 's|<VIRULENCE_DB>|{virulence_db}|' {script_path}")
    run_command(f"sed -i 's|<DATA_DIR>|{data_dir}|' {script_path}")
    run_command(f"sed -i 's|<INPUT_DIR>|{input_dir}|' {script_path}")
    run_command(f"tmux send-keys -t {session_name} 'bash {script_path}' C-m")
    print("VirulenceFinder step completed.")
