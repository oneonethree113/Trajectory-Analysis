# Trajectory Clustering

This repository contains the solution to a technical test involving the clustering of trajectories based on their similarity in direction. The goal of the project is to group trajectories that exhibit similar directions using hierarchical clustering.

## Problem Statement

Given a JSON file containing trajectories, the task is to group these trajectories based on their similarity in direction. Similar trajectories are expected to belong to the same cluster, while trajectories with distinct directions should be assigned to different clusters.

## Solution Overview

To address this problem, I developed a Python script that performs trajectory clustering using hierarchical clustering. Here's how my code works:

1. **Classes**: I created two classes, `Coordinates` and `Trajectory`, to handle the trajectory data and calculate the similarity between trajectories.

2. **Similarity Calculation**: I computed the similarity between trajectories by comparing their directions. The similarity metric was then used as the distance metric for clustering.

3. **Hierarchical Clustering**: I used the hierarchical clustering algorithm provided by the `scikit-learn` library. The calculated similarity was utilized as the distance metric to create clusters of trajectories.

4. **Visualization**: After clustering, I visualized the trajectories using different colors for each cluster. This allows easy identification of the most common trajectory groups.

## Usage

1. Clone this repository to your local machine.
2. Replace the provided JSON file with your own trajectory data.
3. Run the Python script to perform trajectory clustering and generate the visualization.

## Dependencies

- Python (>= 3.x)
- scikit-learn
- matplotlib

## How to Run

```bash
python trajectory_clustering.py
