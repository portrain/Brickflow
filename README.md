# Brickflow - plan your next big brick build
Building big brick projects with friends can easily turn into frustration when everybody wants to contribute at the same time. Quickly, people start fighting over building steps and bricks.
The Brickflow tool avoids those dramas by allowing the master builder to group independent build steps from the build instructions into groups and define their dependencies.
Brickflow then draws a graph of all the build groups. Using a print-out of the graph during the build allows the builders to pick a group that has all its dependencies resolved,
build this group without interfering with other builders and finally tick off the group so everybody can track the progress.

Basically, Brickflow brings project management (think work-breakdown-structure) to building brick models.

## Build definition
Each build is defined in a YAML file. It defines the title of the build, a list of colors that are used to visually identify
the different bags the brick pieces come in and a list of all the build steps grouped into independent units.

The following is an excerpt of the build `millennium.yaml`:

```yaml
title: "Millennium Build"

bagcolors:
  - "cornflowerblue"
  - "darkorchid"
  - "coral"

shapes:
  independent:
    shape: "folder"
    margin: "0.3,0.3"
  integration:
    shape: "octagon"
    margin: "0.1,0.1"

groups:
  # ---------------------------------
  #              Bag 1
  # ---------------------------------
  - start: 1
    end: 31
    bag: 1
    next: 71

  - start: 32
    end: 70
    bag: 1
    next: 71

  - start: 71
    end: 71
    bag: 1
    next: 72
```

Each independent group consists of four fields that are required in order to define the dependencies and draw the graph.

| field       | description |
| -----       | ----- |
| start       | The build step number from the instructions the group starts with |
| end         | The build step number from the instructions the group ends with |
| bag         | The bag number as printed on the bag. Make sure there are at least as many colors defined in `bagcolors` as you have bags. |
| next        | The start step number of the build group that requires this group to be completed |

This definition makes use of the fact that most big brick builds are based around the process of assembling smaller pieces first and then
attaching those to an ever growing model. In order to turn the instructions of a brick set into the definition of the YAML file we found
the following rules helpful:
1. Identify pieces that can be build independently. Often the instructions are already structured such that they show a preview of a
moderately large piece followed by the steps to build it. Use the first and last step number of this piece for a group in the definition file.
2. Find the step that integrates this piece with either the big model or another piece. Use the first step number of this integration step  as the `next` field.
3. If the integration step is only a single build step set the `start` amd `end` field to the same number.
4. The `next` field of an integration step should point to the next integration step in which new, independent pieces are added to the model. 

## Requirements
Brickflow is written in Python and requires Python 3.6+. It uses the networkX library for handling the build group dependency graph and graphviz for drawing.
Its Python dependencies are specified in `requirements.txt`. It has only been tested on Linux, but should also run on Windows and MacOS.

## Run Brickflow

The main file to run Brickflow is `brickflow.py`. In order to see the available options run:
```bash
python brickflow.py --help
```

There are three commands available: `validate`, `print` and `plot`.

### Validate
The `validate` command checks whether the specified definition file is valid and can be processed. It takes the path to the
definition file as its only argument:

```bash
python brickflow.py validate /my/local/data/millennium.yaml
```

### Print
The `print` command prints a dependency resolved build plan to the command line. Under the hood, the graph is topologically sorted
and the first and next step are printed:

```bash
python brickflow.py print /my/local/data/millennium.yaml
```

### Plot
The `plot` command is the main command of Brickflow. It generates an image of the dependency graph. It takes the path to the definition
file as well as the path to the output file image as arguments. It offers two options:
* `--layout` specifies the layout engine of graphviz that should be used. Valid values are: `neato`, `dot`, `twopi`, `circo`, `fdp`, `nop`
* `--format` specifies the output format. If this option is not given, the format will be guessed from the file extension of the `output` path.
Valid values are: `gif`, `jpeg`, `pdf`, `png`, `svg`

```bash
python brickflow.py plot --layout=dot /my/local/data/millennium.yaml /my/local/output/plan.png
```


## Using Docker makes your life a lot easier 
Installing the requirements of Brickflow (particularly graphviz and pygraphviz) can be difficult on platforms such as Windows.
To facilitate the use of Brickflow on those platforms, we recommend to use the provided Dockerfile to run Brickflow in Docker. 

The Docker container exposes three volumes:

| volume      | description |
| -----       | ----- |
| /app | Use this volume to mount a local folder of the brickflow source code inside the container. Only used for development purposes |
| /data | Use this volume to mount a folder with the YAML files |
| /output | Use this volume to mount a folder for storing the output graph images |

Additionally, the Docker container expects the Environment Variable `args` to be set. This variable contains the
arguments that are used for running Brickflow.

### Examples
 
Print the help information:
```bash
docker run --rm brickflow:latest
```

Mount a local data folder and print a text representation of the dependency resolved plan for the `millennium.yaml` file:
```bash
docker run --rm -e "args=print /data/millennium.yaml" -v /my/local/data:/data brickflow
```

Mount a local data and output folder, load the `millennium.yaml` file and create a graph image using the `dot` layout engine:
```bash
docker run --rm -e "args=plot --layout=dot /data/millennium.yaml /output/plan.png" -v /my/local/data:/data -v /my/local/output:/output brickflow
```

Only for development purposes, mount the local source code folder and execute bash:
```bash
docker run --rm -it -v /my/local/code/Brickflow:/app brickflow /bin/bash
```
