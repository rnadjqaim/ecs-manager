
import boto3
from prettytable import PrettyTable

def list_tasks(cluster_name=None, service_name=None, status=None):
    ecs_client = boto3.client('ecs')

    tasks = ecs_client.list_tasks(
        cluster=cluster_name,
        desiredStatus=status.upper() if status else None
    )

    # Get detailed descriptions for the tasks
    task_descriptions = ecs_client.describe_tasks(
        cluster=cluster_name,
        tasks=tasks['taskArns']
    )

    table = PrettyTable()
    table.field_names = ["TASK ID", "SERVICE NAME", "STATUS", "RUNNING COUNT", "LAUNCH TYPE", "AGE"]

    for task in task_descriptions['tasks']:
        task_id = task['taskArn'].split('/')[-1]
        service = task['group']
        task_status = task['lastStatus']
        running_count = f"{task['desiredStatus']}/{task['containers'][0]['exitCode'] if 'exitCode' in task['containers'][0] else '-'}"
        launch_type = task['launchType']
        age = task['createdAt']

        table.add_row([task_id, service, task_status, running_count, launch_type, age])

    print(table)
# ecs_tasks.py

def stop_task(cluster_name, task_id):
    ecs_client = boto3.client('ecs')
    response = ecs_client.stop_task(
        cluster=cluster_name,
        task=task_id
    )
    print(f"Task {task_id} stopped successfully.")

def run_task(cluster_name, task_definition):
    ecs_client = boto3.client('ecs')
    response = ecs_client.run_task(
        cluster=cluster_name,
        taskDefinition=task_definition
    )
    print(f"Task {response['tasks'][0]['taskArn']} started successfully.")

