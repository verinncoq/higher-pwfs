# Towards a Software Framework for Nested Piecewise Functions

by [Andrei Aleksandrov](https://github.com/Zawuza) and [Kim Völlinger](https://github.com/KimVoellinger).

## Overview

A piecewise function is defined by cases over a partitioned domain, such as the sign function 
or rectified linear unit. 
Piecewise functions play a key role in mathematical modeling and computing. 
Despite their practical relevance, their systematic representation as first-class abstractions 
in software systems has received little attention. 
Addressing this gap, we propose a general-purpose, language-independent software framework for 
piecewise functions that supports nesting (i.e. some pieces are again piecewise-defined). 
While mathematically equivalent, nesting provides a hierarchical structure that enables encapsulation 
of evaluation strategies, provides structured representation of complex domain partitions, 
and aligns naturally with software engineering and modeling principles such as modularity and composability.

In the paper, we present resalts of a literature review of mathematical representations, classification schemes,
key application areas and existing software support for piecewise functions. 
We showcase a general framework for piecewise function (`pwfs_framework.py`) that also supports piecewise functions
that have piecewise functions as their segments, called *nested piecewise functions*.

To better explore our framework and nesting, we present three case studies:
1. **Partiton Overlay** focuses on constructing a nested piecewise function that combines a partition assumed to have
    a fast search algorithm with a more general evaluation strategy inside elements of the partiton (`partition_overlay.py`).
2. **Evaluation Selection** showcases how nesting allows a piecewise function to select the most optimal evaluation 
    strategy based on run-time statistics (`evaluation_selection.py`).
3. **Algebraic Operations** demonstrates how algebraic operations can be defined on two "base cases": segment and a piecewise
    function such that the resulting code immediately works for nested piecewise functions as well.
All case studies are supplied with unit tests showing basic use of resulting abstract code.

The paper is currently under review.

## Repository overview

```
│   README.md
│   .gitignore
│   LICENSE
│   .vscode\
│   pwfs_framework.py               <---- Implementation of the framework for piecewise functions
│   partition_overlay.py            <---- Code for case study 1 "Partition Overlay"
│   partiton_overlay_test.py        <---- Unit tests for case study 1
│   evaluation_selection.py         <---- Code for case study 2 "Evaluation Strategy Selection"
|   evaluation_selection_test.py    <---- Unit tests for case study 2
|   algebraic_operations.py         <---- Code for case study 3 "Algebraic Operations"
|   algebraic_operations_test.py    <---- Unit tests for case study 3
```

## Instructions

The code was written using Python 3.13.2

Unit tests can be executed using command line:
```
python -m unittest discover -s . -p "*_test.py"
```
The `.vscode` directory provides test runner configuration for [VS Code Python extension](https://code.visualstudio.com/docs/python/testing).
