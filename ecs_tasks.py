#!/usr/bin/env python3

import click
import boto3
from prettytable import PrettyTable

# Command group for the ECS Manager
@click.group()
def ecs_manager():
    pass

# List tasks command
@ecs_manager.command()
@click.option('--cluster', required=True, help='Name of the ECS cluster')
@click.option('--service', required=False, help='Name of the ECS service')
@click.option('--status', required=False, help='Desired status of the tasks (RUNNING, STOPPED, etc.)')
def list_tasks(cluster, service, status):
    """List ECS tasks in a cluster."""
    ecs_client = boto3.client('ecs')

    tasks = ecs_client.list_tasks(
        cluster=cluster,
        desiredStatus=status.upper() if status else None
    )

    # Get detailed descriptions for the tasks
    task_descriptions = ecs_client.describe_tasks(
        cluster=cluster,
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

# Stop task command
@ecs_manager.command()
@click.option('--cluster', required=True, help='Name of the ECS cluster')
@click.option('--task-id', required=True, help='ID of the task to stop')
def stop_task(cluster, task_id):
    """Stop an ECS task."""
    ecs_client = boto3.client('ecs')
    response = ecs_client.stop_task(
        cluster=cluster,
        task=task_id
    )
    print(f"Task {task_id} stopped successfully.")

# Run task command
@ecs_manager.command()
@click.option('--cluster', required=True, help='Name of the ECS cluster')
@click.option('--task-definition', required=True, help='Task definition to run')
def run_task(cluster, task_definition):
    """Run an ECS task."""
    ecs_client = boto3.client('ecs')
    response = ecs_client.run_task(
        cluster=cluster,
        taskDefinition=task_definition
    )
    print(f"Task {response['tasks'][0]['taskArn']} started successfully.")

# Migrate task command
@ecs_manager.command()
@click.option('--from-cluster', required=True, help='Source cluster name')
@click.option('--to-cluster', required=True, help='Target cluster name (EC2 or Fargate)')
@click.option('--task-definition', required=True, help='Task definition to migrate')
def migrate_task(from_cluster, to_cluster, task_definition):
    """Migrate a task from one cluster to another."""
    ecs_client = boto3.client('ecs')

    # Run task on the new cluster
    response = ecs_client.run_task(
        cluster=to_cluster,
        taskDefinition=task_definition
    )
    new_task_id = response['tasks'][0]['taskArn'].split('/')[-1]

    print(f"Task migrated to {to_cluster}. New task ID: {new_task_id}")

# Main entry point
if __name__ == '__main__':
    ecs_manager()
