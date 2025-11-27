# Ethereum PeerDAS Simulation

This repository contains a Python-based computational model of the **Reed-Solomon Erasure Coding** dependency used in Ethereum's PeerDAS (Data Availability Sampling) roadmap (Fusaka/Fectra).

## Research Note
You can read the full research note and methodology here: **[[Brown Research]](https://hackmd.io/@brownresearch/HJCxnRCAel)**

## Overview
The goal of this simulation is to empirically verify the "Information Theoretic Threshold" of Ethereum blobs. It models:
1.  **Blob Generation:** Creating 128KB mock blobs.
2.  **Extension:** Applying Reed-Solomon encoding (2x expansion).
3.  **Erasure:** Simulating 50% data loss (Network/Proposer failure).
4.  **Reconstruction:** verifying the blob can be restored.

## Files
* `simulation.py`: The core script that runs the encoding/decoding benchmark.

## How to Run
1. Install dependencies:
   ```bash
   !pip install reedsolo
2. Run the simulation:
   ```bash
   simulation.py   
