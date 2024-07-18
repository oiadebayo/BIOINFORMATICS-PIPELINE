import os
from main import run_command


def run_plasmidfinder(species):
    session_name = "plasmidfinder_session"
    plasmid_db = "/data/ghru/databases/plasmidfinder_db/"
    data_dir = "/data/ghru/ghru_retrospective_2018/2020-01-15"
    input_dir = os.path.join(data_dir, "species_fastqs", species)
    output_dir = os.path.join(data_dir, "plasmidfinder_output", species)
    scripts_dir = os.path.join(output_dir, "scripts")
    work_dir = os.path.join(output_dir, "work_dir")
    script_path = os.path.join(scripts_dir, "run_plasmidfinder_for_multiple.sh")
    source_script = "/data/ghru/ghru_retrospective_2018/2020-01-15/templates/run_plasmidfinder_for_multiple.sh"

    os.makedirs(scripts_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)
    run_command("cd /data/ghru/databases/plasmidfinder_db && git pull")
    run_command(f"tmux new -d -s {session_name}")
    run_command(f"cp {source_script} {script_path}")
    run_command(f"sed -i 's/<SPECIES>/{species}/' {script_path}")
    run_command(f"sed -i 's|<PLASMID_DB>|{plasmid_db}|' {script_path}")
    run_command(f"sed -i 's|<INPUT_DIR>|{input_dir}|' {script_path}")
    os.chdir(work_dir)
    work_dir_var = os.getcwd()
    run_command(f"sed -i 's|<WORK_DIR>|{work_dir_var}|' {script_path}")
    run_command(f"tmux send-keys -t {session_name} 'bash {script_path}' C-m")
    print("PlasmidFinder step completed.")
