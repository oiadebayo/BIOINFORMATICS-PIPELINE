import os
from main import run_command


def run_amrfinderplus(species, data_dir):
    session_name = "amrfinderplus_session"
    scripts_dir = os.path.join(data_dir, "scripts")
    script_path = os.path.join(scripts_dir, "run_amrfinder_plus.sh")
    source_script = "/data/ghru/scripts/run_amrfinder_plus.sh"

    os.makedirs(scripts_dir, exist_ok=True)
    run_command(f"tmux new -d -s {session_name}")
    run_command(f"cp {source_script} {script_path}")
    run_command(f"sed -i 's/<SPECIES>/{species}/' {script_path}")
    run_command(f"sed -i 's|<DATA_DIR>|{data_dir}|' {script_path}")
    run_command(f"tmux send-keys -t {session_name} 'bash {script_path}' C-m")
    print("AMRFinderPlus step completed.")
