import json
import hashlib
import inspect
import csv
from pathlib import Path
from typing import Callable, List
from models import Position, Parameters, test_sandbox


HISTORY_ROOT = Path(".results")
SCRIPTS_DIR = HISTORY_ROOT / "scripts"
RESULTS_PER_PAGE = 200
RESULTS_INDEX = HISTORY_ROOT / "index.csv"

def save_test_results(results: List[Position], total_profit: float, sandbox: test_sandbox) -> None:
    script_fn, parameters = sandbox.logic, sandbox.parameters
    script_name, script_hash = _get_script_info(script_fn)
    script_version = _get_or_create_script_version(script_name, script_hash, script_fn)
    result_id = _get_next_result_id()
    results_path = _store_results_json(results, result_id)
    _append_history_entry(
        parameters=parameters,
        result_id=result_id,
        results_path=results_path,
        total_profit=total_profit,
        script_name=script_name,
        script_version=script_version,
        script_hash=script_hash
    )


def get_results_history(page: int = 1) -> List[dict]:
    """Fetches paginated history data from the results index."""
    # Open the index file
    with RESULTS_INDEX.open("r", newline='') as f:
        reader = csv.DictReader(f)
        history_entries = [row for row in reader]

    # Calculate pagination indices
    page_start = (page - 1) * RESULTS_PER_PAGE
    page_end = page_start + RESULTS_PER_PAGE

    # Slice the history entries for the requested page
    paginated_entries = history_entries[page_start:page_end]

    # Convert the results to a list of dictionaries with proper formatting
    return [
        {
            "result_id": int(entry["result_id"]),
            "results_path": entry["results_path"],
            "total_profit": float(entry["total_profit"]),
            "script_name": entry["script_name"],
            "script_version": int(entry["script_version"]),
            "script_hash": entry["script_hash"],
            "script_path": entry["script_path"],
            "parameters": Parameters.from_string(entry["parameters"]),
        }
        for entry in paginated_entries
    ]




def get_results_by_id(result_id: int) -> List[Position]:
    """Fetches the results JSON file for a given result_id."""
    # Determine the range folder
    page_start = ((result_id - 1) // RESULTS_PER_PAGE) * RESULTS_PER_PAGE + 1
    page_end = page_start + RESULTS_PER_PAGE - 1
    result_folder = HISTORY_ROOT / f"{page_start}-{page_end}"

    # Construct the file path for the result
    result_file = result_folder / f"results_{result_id}.json"

    # Read and return the JSON data
    with result_file.open("r") as f:
        return json.load(f)
    

# ──────────────────────────── SUBFUNCTIONS ────────────────────────────

def _get_script_info(script_fn: Callable) -> tuple[str, str]:
    script_name = script_fn.__name__
    script_source = inspect.getsource(script_fn).strip()
    script_hash = hashlib.sha256(script_source.encode("utf-8")).hexdigest()
    return script_name, script_hash


def _get_or_create_script_version(script_name: str, script_hash: str, script_fn: Callable) -> int:
    # Ensure base directory for scripts exists
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    # Script-specific folder and local index
    script_folder = SCRIPTS_DIR / script_name
    script_folder.mkdir(parents=True, exist_ok=True)
    script_local_index = script_folder / "index.csv"
    script_local_index.touch(exist_ok=True)

    # Load existing versions from local index
    existing_versions = {}
    with script_local_index.open("r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_versions[row["script_hash"]] = int(row["version"])

    # Return version if hash already exists
    if script_hash in existing_versions:
        return existing_versions[script_hash]

    # Else: create a new version
    version = max(existing_versions.values(), default=0) + 1
    script_path = script_folder / f"v{version}.py"
    with open(script_path, "w") as f:
        f.write(inspect.getsource(script_fn).strip())

    # Append to local script index
    with script_local_index.open("a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["script_hash", "version", "script_path"])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "script_hash": script_hash,
            "version": version,
            "script_path": str(script_path)
        })

    return version


def _get_next_result_id() -> int:
    HISTORY_ROOT.mkdir(parents=True, exist_ok=True)
    RESULTS_INDEX.touch(exist_ok=True)

    with RESULTS_INDEX.open("r", newline='') as f:
        reader = csv.DictReader(f)
        ids = [int(row["result_id"]) for row in reader]
    return max(ids, default=0) + 1


def _store_results_json(results: List[dict], result_id: int) -> str:
    page_start = ((result_id - 1) // RESULTS_PER_PAGE) * RESULTS_PER_PAGE + 1
    page_end = page_start + RESULTS_PER_PAGE - 1
    folder_name = f"{page_start}-{page_end}"
    result_folder = HISTORY_ROOT / folder_name
    result_folder.mkdir(parents=True, exist_ok=True)

    results_path = result_folder / f"results_{result_id}.json"
    with open(results_path, "w") as f:
        json.dump(results, f, default=str, indent=2)
    return str(results_path)


def _append_history_entry(result_id: int, results_path: str, total_profit: float,
                          script_name: str, script_version: int, 
                          script_hash: str, parameters: Parameters) -> None:
    RESULTS_INDEX.touch(exist_ok=True)
    with RESULTS_INDEX.open("a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "result_id", "results_path", "total_profit",
            "script_name", "script_version", "script_hash", "script_path", "parameters"
        ])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            "result_id": result_id,
            "results_path": results_path,
            "total_profit": total_profit,
            "script_name": script_name,
            "script_version": script_version,
            "script_hash": script_hash,
            "script_path": f"scripts/{script_name}/v{script_version}.py",
            "parameters": parameters
        })





