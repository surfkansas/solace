import boto3
import datetime

devices_metadata = [
    {
        'name': 'Amazon Web Services — SV1',
        'description': 'Amazon Braket state vector simulator',
        's3_folder_key': 'aws-simulator',
        'type': 'simulator',
        'location': 'AWS',
        'qubits': 34,
        'regions': ['us-east-1', 'us-west-1', 'us-west-2'],
        'arn': 'arn:aws:braket:::device/quantum-simulator/amazon/sv1',
        'cost': '$0.075 / minute'
    },
    {
        'name': 'Amazon Web Services — TN1',
        'description': 'Amazon Braket tensor network simulator',
        's3_folder_key': 'aws-simulator',
        'type': 'simulator',
        'location': 'AWS',
        'qubits': 50,
        'regions': ['us-east-1', 'us-west-2'],
        'arn': 'arn:aws:braket:::device/quantum-simulator/amazon/tn1',
        'cost': '$0.275 / minute'
    },
    {
        'name': 'D-Wave — Advantage_system1.1',
        'description': 'Quantum Annealer based on superconducting qubits',
        's3_folder_key' : 'dwave',
        'type': 'annealer',
        'location': 'British Columbia, Canada',
        'qubits': 5760,
        'regions': ['us-west-2'],
        'arn': 'arn:aws:braket:::device/qpu/d-wave/Advantage_system1',
        'cost': '$0.30 / task + $0.00019 / shot'
    },
    {
        'name': 'D-Wave — DW_2000Q_6',
        'description': 'Quantum Annealer based on superconducting qubits',
        's3_folder_key' : 'dwave',
        'type': 'annealer',
        'location': 'British Columbia, Canada',
        'qubits': 2048,
        'regions': ['us-west-2'],
        'arn': 'arn:aws:braket:::device/qpu/d-wave/DW_2000Q_6',
        'cost': '$0.30 / task + $0.00019 / shot'
    },
    {
        'name': 'IonQ',
        'description': 'Universal gate-model QPU based on trapped ions',
        's3_folder_key' : 'ionq',
        'type': 'gate_model',
        'qubits': 11,
        'regions': ['us-east-1'],
        'location': 'Maryland, USA',
        'arn': 'arn:aws:braket:::device/qpu/ionq/ionQdevice',
        'cost': '$0.30 / task + $0.01 / shot',
        'availability': {
            'day_of_week': 'Weekdays',
            'start_time': '13:00:00',
            'end_time': '21:00:00'
        }
    },
    {
        'name': 'Rigetti — Aspen-9',
        'description': 'Universal gate-model QPU based on superconducting qubits',
        's3_folder_key': 'rigetti',
        'type': 'gate_model',
        'qubits': 31,
        'regions': ['us-west-1'],
        'location': 'California',
        'arn': 'arn:aws:braket:::device/qpu/rigetti/Aspen-9',
        'cost': '$0.30 / task + $0.00035 / shot',
        'availability': {
            'day_of_week': 'Everyday',
            'start_time': '15:00:00',
            'end_time': '19:00:00'
        }
    }
]

def get_device_from_selection(simulator = False, annealer = False, gate_model = False):
    matched_devices_metadata = []
    for device_metadata in devices_metadata:
        if simulator and device_metadata['type'] == 'simulator':
            matched_devices_metadata.append(device_metadata)
        if annealer and device_metadata['type'] == 'annealer':
            matched_devices_metadata.append(device_metadata)
        if gate_model and device_metadata['type'] == 'gate_model':
            matched_devices_metadata.append(device_metadata)

    print()
    print('Please choose your Quantum device from the list below...')
    
    device_num = -1
    for matched_device_metadata in matched_devices_metadata:
        device_num += 1
        print()
        print(f' {device_num} :: {matched_device_metadata["name"]}')
        print(f'      {matched_device_metadata["description"]}')
        print(f'        Qubits       : {matched_device_metadata["qubits"]}')
        print(f'        Regions      : {matched_device_metadata["regions"]}')
        print(f'        Location     : {matched_device_metadata["location"]}')
        print(f'        Cost         : {matched_device_metadata["cost"]}')
        if 'availability' in matched_device_metadata:
            print(f'        Availability : {matched_device_metadata["availability"]["day_of_week"]}')
            print(f'                       {matched_device_metadata["availability"]["start_time"]} - {matched_device_metadata["availability"]["end_time"]} UTC')
            available = True
            if datetime.datetime.today().weekday() > 5 and matched_device_metadata["availability"]["day_of_week"] == 'Weekdays':
                available = False
            current_time_utc = datetime.datetime.utcnow().strftime('%H:%M:%S')
            if current_time_utc < matched_device_metadata["availability"]["start_time"]:
                available = False
            if current_time_utc > matched_device_metadata["availability"]["end_time"]:
                available = False
            if available == False:
                print(f'                       Currently Unavailable')
    print()

    selected = -1
    while selected == -1:
        input_value = input('Enter selection number: ')
        if input_value.isdigit():
            input_int = int(input_value)
            if input_int >= 0 and input_int < len(matched_devices_metadata):
                selected = input_int
    
    return matched_devices_metadata[selected]['arn'], get_s3_folder(matched_devices_metadata[selected]['s3_folder_key'])

def get_s3_folder(s3_folder_key):
    aws_account_id = boto3.client("sts").get_caller_identity()['Account']
    return (f'amazon-braket-output-{aws_account_id}', s3_folder_key)

