#!/usr/bin/env python3

import braketology
from braket.aws import AwsDevice
from braket.circuits import Circuit

# Lookup the the 
device_arn, s3_folder = braketology.get_device_from_selection(simulator = True, gate_model = True)

# Create the AWS quantum device
device = AwsDevice(device_arn)

# Create the quantum circuit. This quantum circuit puts both the first
# qubit into a superposition state using an H gate, and then entangles
# it with second qubit using a CNOT gate.
circuit = Circuit().h(0).cnot(0, 1)
print()
print('The following circuit will be submitted to AWS Braket...')
print()
print(circuit)
print()

# Run the task on the selected device
print('Running bell state circuit with 100 shots')
task = device.run(circuit, s3_folder, shots=100)
results = task.result()

# Output observations
print('Task completed with the following measurements:')
print()
print('  measurement ║    count    ')
print(' ═════════════╬═════════════')
for measurement in sorted(results.measurement_counts):
    print(f'      {measurement}      ║     {results.measurement_counts[measurement]}')
print()