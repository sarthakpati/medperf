import typer
from typing import Optional

import medperf.config as config
from medperf.decorators import clean_except
from medperf.entities.benchmark import Benchmark
from medperf.commands.list import EntityList
from medperf.commands.view import EntityView
from medperf.commands.benchmark.submit import SubmitBenchmark
from medperf.commands.benchmark.associate import AssociateBenchmark
from medperf.commands.result.create import BenchmarkExecution

app = typer.Typer()


@app.command("ls")
@clean_except
def list(
    local: bool = typer.Option(False, "--local", help="Get local benchmarks"),
    mine: bool = typer.Option(False, "--mine", help="Get current-user benchmarks"),
):
    """List benchmarks stored locally and remotely from the user"""
    EntityList.run(
        Benchmark,
        fields=["UID", "Name", "Description", "State", "Approval Status", "Registered"],
        local_only=local,
        mine_only=mine,
    )


@app.command("submit")
@clean_except
def submit(
    name: str = typer.Option(..., "--name", "-n", help="Name of the benchmark"),
    description: str = typer.Option(
        ..., "--description", "-d", help="Description of the benchmark"
    ),
    docs_url: str = typer.Option("", "--docs-url", "-u", help="URL to documentation"),
    demo_url: str = typer.Option(
        "",
        "--demo-url",
        help="""Identifier to download the demonstration dataset tarball file.\n
        See `medperf mlcube submit --help` for more information""",
    ),
    demo_hash: str = typer.Option(
        "", "--demo-hash", help="SHA1 of demonstration dataset tarball file"
    ),
    data_preparation_mlcube: int = typer.Option(
        ..., "--data-preparation-mlcube", "-p", help="Data Preparation MLCube UID"
    ),
    reference_model_mlcube: int = typer.Option(
        ..., "--reference-model-mlcube", "-m", help="Reference Model MLCube UID"
    ),
    evaluator_mlcube: int = typer.Option(
        ..., "--evaluator-mlcube", "-e", help="Evaluator MLCube UID"
    ),
):
    """Submits a new benchmark to the platform"""
    benchmark_info = {
        "name": name,
        "description": description,
        "docs_url": docs_url,
        "demo_dataset_tarball_url": demo_url,
        "demo_dataset_tarball_hash": demo_hash,
        "data_preparation_mlcube": data_preparation_mlcube,
        "reference_model_mlcube": reference_model_mlcube,
        "data_evaluator_mlcube": evaluator_mlcube,
    }
    SubmitBenchmark.run(benchmark_info)
    config.ui.print("✅ Done!")


@app.command("associate")
@clean_except
def associate(
    benchmark_uid: int = typer.Option(
        ..., "--benchmark_uid", "-b", help="UID of benchmark to associate with"
    ),
    model_uid: int = typer.Option(
        None, "--model_uid", "-m", help="UID of model MLCube to associate"
    ),
    dataset_uid: int = typer.Option(
        None, "--data_uid", "-d", help="Server UID of registered dataset to associate"
    ),
    approval: bool = typer.Option(False, "-y", help="Skip approval step"),
    no_cache: bool = typer.Option(
        False, "--no-cache", help="Execute the test even if results already exist",
    ),
):
    """Associates a benchmark with a given mlcube or dataset. Only one option at a time.
    """
    AssociateBenchmark.run(
        benchmark_uid, model_uid, dataset_uid, approved=approval, no_cache=no_cache
    )
    config.ui.print("✅ Done!")


@app.command("run")
@clean_except
def run(
    benchmark_uid: int = typer.Option(
        ..., "--benchmark", "-b", help="UID of the desired benchmark"
    ),
    data_uid: int = typer.Option(
        ..., "--data_uid", "-d", help="Registered Dataset UID"
    ),
    file: str = typer.Option(
        None,
        "--models-from-file",
        "-f",
        help="""A file containing the model UIDs to be executed.\n
        The file should contain a single line as a list of\n
        comma-separated integers corresponding to the model UIDs""",
    ),
    ignore_model_errors: bool = typer.Option(
        False,
        "--ignore-model-errors",
        help="Ignore failing model cubes, allowing for possibly submitting partial results",
    ),
    no_cache: bool = typer.Option(
        False, "--no-cache", help="Execute even if results already exist",
    ),
):
    """Runs the benchmark execution step for a given benchmark, prepared dataset and model
    """
    BenchmarkExecution.run(
        benchmark_uid,
        data_uid,
        models_uids=None,
        no_cache=no_cache,
        models_input_file=file,
        ignore_model_errors=ignore_model_errors,
        show_summary=True,
        ignore_failed_experiments=True,
    )
    config.ui.print("✅ Done!")


@app.command("view")
@clean_except
def view(
    entity_id: Optional[int] = typer.Argument(None, help="Benchmark ID"),
    format: str = typer.Option(
        "yaml",
        "-f",
        "--format",
        help="Format to display contents. Available formats: [yaml, json]",
    ),
    local: bool = typer.Option(
        False,
        "--local",
        help="Display local benchmarks if benchmark ID is not provided",
    ),
    mine: bool = typer.Option(
        False,
        "--mine",
        help="Display current-user benchmarks if benchmark ID is not provided",
    ),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file to store contents. If not provided, the output will be displayed",
    ),
):
    """Displays the information of one or more benchmarks
    """
    EntityView.run(entity_id, Benchmark, format, local, mine, output)
