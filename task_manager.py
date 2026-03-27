import json
import os
import argparse

FILE_NAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {} # Returns empty if the file is corrupted
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, title, priority, deadline):
    # Create a unique ID based on the highest existing ID
    task_id = str(max([int(i) for i in tasks.keys()], default=0) + 1)
    
    tasks[task_id] = {
        "title": title,
        "priority": priority or "Medium",
        "deadline": deadline or "None",
        "status": "Incomplete"
    }
    save_tasks(tasks)
    print(f"✅ Added Task [{task_id}]: {title}")

def list_tasks(tasks):
    if not tasks:
        print("📭 No tasks found.")
        return
    
    print(f"{'ID':<5} {'Task':<20} {'Priority':<10} {'Deadline':<12} {'Status'}")
    print("-" * 60)
    for tid, t in tasks.items():
        print(f"{tid:<5} {t['title']:<20} {t['priority']:<10} {t['deadline']:<12} {t['status']}")

def main():
    tasks = load_tasks()
    parser = argparse.ArgumentParser(description="Pro Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command: add
    add_p = subparsers.add_parser("add")
    add_p.add_argument("title", type=str)
    add_p.add_argument("--priority", choices=["High", "Medium", "Low"])
    add_p.add_argument("--deadline", type=str)

    # Command: list
    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.command == "add":
        add_task(tasks, args.title, args.priority, args.deadline)
    elif args.command == "list":
        list_tasks(tasks)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()