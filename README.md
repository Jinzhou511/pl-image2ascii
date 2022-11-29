# imageto_ascii

[![Version](https://img.shields.io/docker/v/fnndsc/pl_image2ascii?sort=semver)](https://hub.docker.com/r/fnndsc/pl_image2ascii)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl_image2ascii)](https://github.com/FNNDSC/pl_image2ascii/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl_image2ascii/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl_image2ascii/actions/workflows/ci.yml)



## Abstract

`pl_image2ascii` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in jpg images as input files and
creates the ascii art of the jpg image as output files.

## Installation

`pl_image2ascii` is a _[ChRIS](https://chrisproject.org/) ds-type plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://ipfs.babymri.org/ipfs/QmaQM9dUAYFjLVn3PpNTrpbKVavvSTxNLE5BocRCW1UoXG/light.png)](https://chrisstore.co/plugin/pl_image2ascii)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl_image2ascii` as a container:

```shell
singularity exec docker://fnndsc/pl_image2ascii imagetoascii [--args values...] input/ output/
```

To print its available options, run:

```shell
singularity exec docker://fnndsc/pl_image2ascii imagetoascii --help
```

## Examples

`imagetoascii` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
singularity exec docker://fnndsc/pl_image2ascii:latest imagetoascii [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl_image2ascii .
```

### Running

Mount the source code `imagetoascii.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/imagetoascii.py:/usr/local/lib/python3.10/site-packages/imagetoascii.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl_image2ascii imagetoascii /incoming /outgoing
```



## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl_image2ascii:1.2.3 .
docker push docker.io/fnndsc/pl_image2ascii:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl_image2ascii:dev chris_plugin_info > chris_plugin_info.json
```
