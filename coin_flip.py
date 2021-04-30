#!/usr/bin/env python3

import braketology
from braket.aws import AwsDevice
from braket.circuits import Circuit

# Lookup the the 
device_arn, s3_folder = braketology.get_device_from_selection(simulator = True, gate_model = True)

# Create the AWS quantum device
device = AwsDevice(device_arn)

# Create the quantum circuit. This quantum circuit puts both qubits into a 
# superposition state using an H gate.
circuit = Circuit().h(0).h(1)
print()
print('The following circuit will be submitted to AWS Braket...')
print()
print(circuit)
print()

# Run the task on the selected device
print('Running superposition circuit with 100 shots')
task = device.run(circuit, s3_folder, shots=100)
task_metadata = task.metadata()
s3_output = f's3://{task_metadata["outputS3Bucket"]}/{task_metadata["outputS3Directory"]}/results.json'
print()
print(f'Output will be saved to...')
print(s3_output)
print()
results = task.result()

# Output observations
print('Task completed with the following measurements:')
print()
print('  measurement ║    count    ')
print(' ═════════════╬═════════════')
for measurement in sorted(results.measurement_counts):
    print(f'      {measurement}      ║     {results.measurement_counts[measurement]}')
print()