---
name: Evaluator MLCube
url: https://github.com/mlcommons/medperf/examples/HelloWorld/evaluator
slug: evaluator
---
# {{ page.meta.name }}

## Purpose
{{ page.meta.name }}s are responsible of measuring the performance of a model on a given task. These MLCubes compare the prediction generated by the model on prepared data, with the given labels or expected output for such data.

{% include "mlcubes/shared/hello_world.md" %}

{% include "mlcubes/shared/setup.md" %}

### Running the Evaluate Task
{{ page.meta.name }}s have only one purpose, which is to evaluate the model's performance. For this, a evaluator MLCube must provide a `evaluate` task. This task takes in the predictions generated by a Model MLCube, and the labels prepared by the Data Preparator MLCube, and computes evaluator 

1. Check the predictions
    ```bash
    cat workspace/predictions/predictions.csv
    ```
    ```csv title="predictions/predictions.csv"
    --8<-- "examples/HelloWorld/evaluator/mlcube/workspace/predictions/predictions.csv"
    ```

2. Check the labels
    ```bash
    cat workspace/labels/labels.csv
    ```
    ```csv title="labels/labels.csv"
    --8<-- "examples/HelloWorld/evaluator/mlcube/workspace/labels/labels.csv"
    ```
    As you can see, the labels and predictions look pretty much alike. The intent of the {{ page.meta.name }} is to provide such insights in a computational manner. Let's have a look at that

3. Run the `evaluate` task with mlcube:
    ``` bash
    mlcube run --task=evaluate
    ```

4. View the results in the `results.yaml` file using
    ``` bash
    cat workspace/results.yaml
    ```
    ```yaml title="workspace/results.yaml"
    --8<-- "examples/HelloWorld/evaluator/mlcube/workspace/results.yaml"
    ```

That's it! You just built and ran a hello-world {{ page.meta.name }}! Now it's time to build one from scratch.

{% include "mlcubes/shared/build.md" %}

```bash
$ medperf mlcube create evaluator
MedPerf 0.0.0
project_name [Evaluator MLCube]: Hello World Evaluator MLCube # (1)!
project_slug [hello_world_evaluator_mlcube]: evaluator_mlcube # (2)!
description [Evaluator MLCube Template. Provided by MLCommons]: Hello World Evaluator implementation from scratch # (3)!
author_name [John Smith]: John Smith # (4)!
accelerator_count [0]: 0 # (5)!
docker_image_name [docker/image:latest]: johnsmith/hello_world_evaluator:0.0.1 # (6)!
```

1. Gives a Human-readable name to the MLCube Project.
2. Determines how the Data Preparator root folder will be named.
3. Gives a Human-readable description to the MLCube Project.
4. Documents the MLCube implementation by specifying the author. Please use your own name here.
5. Indicates how many GPUs should be visible by the MLCube. Useful for Model MLCubes.
6. MLCubes use containers under the hood. Medperf supports both Docker and Singularity. Here, you can provide an image tag to the image that will be created by this MLCube. **It's recommended to use a naming convention that allows you to upload it to Docker Hub.**

{% include "mlcubes/shared/cookiecutter.md" %}

### Contents
Lets have a look at what the previous command generated. First, lets look at the whole folder structure:
```bash
tree
```
```bash
.
└── evaluator_mlcube
    ├── mlcube
    │   ├── mlcube.yaml # (1)!
    │   └── workspace # (2)!
    │       ├── labels # (3)!
    │       ├── parameters.yaml # (4)!
    │       └── predictions # (5)!
    └── project # (6)!
        ├── Dockerfile # (7)!
        ├── mlcube.py # (8)!
        └── requirements.txt # (9)!

7 directories, 5 files
```

1. The `mlcube.yaml` file contains metadata about your evaluator mlcube, including its interface. For MedPerf, we require a single tasks: `evaluate`.
2. The `workspace` contains all the files and paths that can be used by the MLCube, as long as those paths are specified inside the `mlcube.yaml`.
3. The `labels` folder is where the prepared labels should be contained. These labels come directly from the data preparation mlcube.
4. This file provides ways to parameterize the data preparation process. You can set any key-value pairs that should be easily modifiable to adjust your mlcube's behavior. This file is mandatory but can be left blank if parametrization is unnecessary.
5. The `predictions` folder is where predictions obtained from the model mlcube are contained.
6. Contains the actual implementation code of the mlcube.
7. A default `Dockerfile` which by default installs `python3.6` and any requirements for this MLCube to work.
8. `mlcube.py` provides a bare-bones command-line interface for a Data Preparator MLcube to run. The logic inside each command is intentionally left blank.
9. `requirements.txt` is a common file for python projects, which specifies the dependencies that must be installed to run the project.

Let's go through each of the created files and modify them as needed to create a Hello World {{ page.meta.name }}.

#### `mlcube/mlcube.yaml`
The `mlcube.yaml` file contains metadata about the mlcube tasks.
   
``` yaml title="mlcube.yaml"
name: Hello World Evaluator MLCube # (1)!
description: Hello World Evaluator implementation from scratch # (2)!
authors:
 - {name: John Smith} # (3)!

platform:
  accelerator_count: 0 # (4)!

docker:
  # Image name
  image: johnsmith/hello_world_evaluator:0.0.1 # (5)!
  # Docker build context relative to $MLCUBE_ROOT. Default is `build`.
  build_context: "../project"
  # Docker file name within docker build context, default is `Dockerfile`.
  build_file: "Dockerfile"

tasks:
  evaluate: # (6)!
  # Computes evaluation metrics on the given predictions and ground truths
    parameters: 
      inputs: {
        predictions: predictions, # (7)!
        labels: labels, # (8)!
        parameters_file: parameters.yaml # (9)!
      }
      outputs: {
        output_path: {type: "file", default: "results.yaml"} # (10)!
      }
```

1. This is the name we gave during the configuration procedure.
2. This is the description we provided before.
3. Here you can see a list of authors. It is populated with the given author during setup.
4. The accelerator count defines the number of GPUS that should be visible by the MLCube. This was filled during setup.
5. This is the docker image name we provided before.
6. The evaluate task takes in prepared labels from the Data Preparator MLCube, and predictions from the Model MLCube, and computes performance metrics.
7. **Required**. Where to find the model predictions. **MUST** be a folder.
8. **Required**. Where to find the prepared labels. **MUST** be a folder.
9. **Required**. Helper file to provide additional arguments. Value **MUST** be `parameters.yaml`
11. **Required**. Where to store the performances metrics. Value **MUST** be a `results.yaml`.

The `mlcube.yaml` generated by the template is probably sufficient for this task, so we won't be modifying it.
---
### `mlcube/workspace/parameters.yaml`

This file provides ways to parameterize your model. You can set any key-value pairs that should be easily modifiable to adjust your model's behavior. For this demonstration, we're not going to parametrize this metrics, and instead hardcode the expected behavior. If you want to see a parametrized implementation, check out the [Hello World evaluator's implementation]({{ url }})

---
### `project/mlcube.py`
   
MLCube expects an entry point to the project to run the code and the specified tasks. It expects this entry point to behave like a CLI, in which each MLCube task (e.g., `evaluate`) is executed as a subcommand – and each input/output parameter is passed as a CLI argument. 

An example of the expected interface is:

```bash
python3 project/mlcube.py evaluate --predictions=<PREDICTIONS_PATH>  --labels=<LABELS_PATH> --parameters_file=<PARAMETERS_FILE> --output_path=<OUTPUT_PATH>
```

!!! note 
    You can implement such a CLI interface with any language or tool as long as you follow the command structure demonstrated above.

```python title="mlcube.py"
"""MLCube handler file"""
import typer


app = typer.Typer()


@app.command("evaluate")
def prepare(
    labels: str = typer.Option(..., "--labels"),
    predictions: str = typer.Option(..., "--predictions"),
    parameters_file: str = typer.Option(..., "--parameters_file"),
    output_path: str = typer.Option(..., "--output_path"),
):
    # Modify the prepare command as needed
    raise NotImplementedError("The evaluate method is not yet implemented")


@app.command("hotfix")
def hotfix():
    # NOOP command for typer to behave correctly. DO NOT REMOVE OR MODIFY
    pass


if __name__ == "__main__":
    app()
```

{% include "mlcubes/shared/hotfix.md" %}

---
##### Implement the Evaluate task
The evaluate task should take in a path for prepared labels, as well as for predictions, and output metrics results over that pair. For real tasks, general metrics like Accuracy, F1 Score, or task-specific metrics like Hausdorff95, would be used.

For this example, we will only implement the Accuracy metric, and use the parametrization provided by `parameters.yaml` to compute the results.

```python title="project/mlcube.py"
import os # (1)!
import yaml
import pandas as pd


class ACC: # (2)!
    @staticmethod
    def run(labels, preds):
        total_count = len(labels)
        correct_count = (labels == preds).sum()
        return correct_count / total_count

@app.command("evaluate")
def prepare(
    labels: str = typer.Option(..., "--labels"),
    predictions: str = typer.Option(..., "--predictions"),
    parameters_file: str = typer.Option(..., "--parameters_file"),
    output_path: str = typer.Option(..., "--output_path"),
):
    # Modify the prepare command as needed
    labels_file = os.path.join(labels, "labels.csv")
    predictions_file = os.path.join(predictions, "predictions.csv")

    # Load all files
    labels = pd.read_csv(labels_file)
    preds = pd.read_csv(predictions_file)

    labels = labels.set_index("id").sort_index()
    preds = preds.set_index("id").sort_index()

    results = {}
    score = ACC.run(labels, preds) # (3)!
    results["ACC"] = {"greeting": float(score["greeting"])}

    with open(output_path, "w") as f: # (4)!
        yaml.dump(results, f)
```
1. The necessary imports for this function are provided here, but please place them at the top of your file.
2. Implementation of the Accuracy metric. Given this is a toy example, the metric is implemented by hand. It is recommended that metrics are obtained from trusted libraries.
3. Here we obtain accuracy results from the labels and predictions.
4. The output path is already a file, so we can open it directly.

---
##### The complete implementation
Here you can find the whole `mlcube.py` file after all the implementation changes we made
```python title="project/mlcube.py"
"""MLCube handler file"""
import os
import yaml
import typer
import pandas as pd


app = typer.Typer()


class ACC:
    @staticmethod
    def run(labels, preds):
        total_count = len(labels)
        correct_count = (labels == preds).sum()
        return correct_count / total_count


@app.command("evaluate")
def prepare(
    labels: str = typer.Option(..., "--labels"),
    predictions: str = typer.Option(..., "--predictions"),
    parameters_file: str = typer.Option(..., "--parameters_file"),
    output_path: str = typer.Option(..., "--output_path"),
):
    # Modify the prepare command as needed
    labels_file = os.path.join(labels, "labels.csv")
    predictions_file = os.path.join(predictions, "predictions.csv")

    # Load all files
    labels = pd.read_csv(labels_file)
    preds = pd.read_csv(predictions_file)

    labels = labels.set_index("id").sort_index()
    preds = preds.set_index("id").sort_index()

    results = {}
    score = ACC.run(labels, preds)
    results["ACC"] = {"greeting": float(score["greeting"])}

    with open(output_path, "w") as f:
        yaml.dump(results, f)


@app.command("hotfix")
def hotfix():
    # NOOP command for typer to behave correctly. DO NOT REMOVE OR MODIFY
    pass


if __name__ == "__main__":
    app()
```

---

{% include "mlcubes/shared/docker_file.md" %}

---

{% include "mlcubes/shared/requirements.md" %}

```python title="project/requirements.txt"
# Add your dependencies here
typer
PyYAML
pandas
```

---
That's it! With that, we should have a function {{ page.meta.name }}, that has been implemented for our Hello World Task. Congratulations!

{% include "mlcubes/shared/execute.md" %}

3. Provide labels to your mlcube. In this case, we can use the labels from the Data Preparation tutorial.
    ```bash
    echo "id,greeting\n0,\"Hello, John smith\"\n1,\"Howdy, John Smith\"\n2,\"Greetings, John Smith\"\n3,\"Bonjour, John Smith\"" >> workspace/labels/labels.csv
    ```
    This will create the prepared labels file. You can inspect it with
    ```bash
    cat workspace/labels/labels.csv
    ```
    ```bash title="workspace/labels/labels.csv"
    id,greeting
    0,"Hello, John smith"
    1,"Howdy, John Smith"
    2,"Greetings, John Smith"
    3,"Bonjour, John Smith"
    ```
4. Provide predictions to your mlcube. We could use the same file as before, but to make it insteresting let's add a small error to the data.
    ```bash
    echo "id,greeting\n0,\"Hello, John smith\"\n1,\"Heyo, John Smith\"\n2,\"Greetings, John Smith\"\n3,\"Bonjour, John Smith\"" >> workspace/predictions/predictions.csv
    ```
    This will create a predictions file. You can inspect it with
    ```bash
    cat workspace/predictions/predictions.csv
    ```
    ```bash title="workspace/predictions/predictions.csv"
    id,greeting
    0,"Hello, John smith"
    1,"Heyo, John Smith"
    2,"Greetings, John Smith"
    3,"Bonjour, John Smith" 
    ```
    Notice that the `Howdy` greeting was replace with `Heyo`. Let's see what our metrics cube says about this.
5. Run the pipeline. If you want details of what is going on at each step, look for the [How to run](#how-to-run) section.
    ```bash
    mlcube run --task=evaluate
    ```
That's it! You should now be able to write your own {{ page.meta.name }} from scratch!