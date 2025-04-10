QRLE: Quantum Run-length Encoding for Resource-efficient Data Representation
This repository contains the code and data accompanying the paper:

"Design and Implementation of Run-length Encoding on Quantum Computers for Resource-efficient Data Representation"
(submitted to Applied Soft Computing)

📄 Overview
This project implements and evaluates a quantum version of run-length encoding (QRLE), aiming at resource-efficient data representation on quantum computers. The repository includes:

All code and datasets used in the experiments of the paper.

Test results from both quantum simulators and real superconducting quantum devices (IBM Quantum).

Modular and reusable implementation of the QRLE circuit generation.

📁 Repository Structure
Noise/
Contains the experiments analyzing the impact of quantum noise as discussed in the paper.

Real_Vs_simulator_test/
Includes comparison experiments between quantum simulators and IBM’s real superconducting quantum computer (ibm_sherbrooke).

Three .xlsx files present the raw results returned from IBM Quantum backends.

qrle_module.py
Provides a QRLE class with general functions to generate QRLE circuits based on input datasets. Can be reused for custom datasets.

requirements.txt
Lists all Python libraries required to run the experiments.

⚙️ Requirements
To install all necessary dependencies:

pip install -r requirements.txt
🧪 Running Experiments
You can run the provided scripts to reproduce the experiments from the paper, or use the QRLE class to build your own quantum circuits for run-length encoding.


