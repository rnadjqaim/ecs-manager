ECS Manager CLI Tool

Overview


Alright, so this is a CLI tool for managing ECS tasks, both for EC2 and Fargate. It’s kinda like the AWS ECS CLI, but with some extra features. You can list tasks, run and stop them, and even migrate tasks between EC2 and Fargate. If you're using ECS for these, this tool will hopefully make your life a bit easier.

Key Features:
List tasks similar to kubectl get pods (if you’ve used Kubernetes, you’ll get it).
You can run tasks, stop them, or even pause them (though technically you stop them and start again later).
Oh, and you can migrate tasks between EC2 and Fargate seamlessly.
Commands
Here are some of the basic commands. They’re simple, but they do what you need.

List tasks in a cluster:

bash
Copy code
ecs-manager get tasks --cluster my-cluster --status RUNNING
It’ll list task IDs, service names, statuses, and some other useful details.

Run a task:

bash
Copy code
ecs-manager task run --cluster my-cluster --task-definition my-task-def
Starts a new task based on the provided task definition.

Stop a task:

bash
Copy code
ecs-manager task stop --cluster my-cluster --task-id <task-id>
Stops the task. No questions asked.

Migrate task (between EC2 and Fargate):

bash
Copy code
ecs-manager task migrate --from ec2-cluster --to fargate-cluster --task-id <task-id>
Moves a task from EC2 to Fargate 
