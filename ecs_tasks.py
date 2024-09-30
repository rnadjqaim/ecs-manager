
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
