

from taskforge.task import Task
from taskforge.task_manager import TaskManager

tm = TaskManager()

while True:
    print("\n--- TaskForge ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Delete Task")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        title = input("Task title: ")
        deadline = input("Deadline (YYYY-MM-DD): ")
        priority = input("Priority (Low/Medium/High): ")
        task = Task(title=title, deadline=deadline, priority=priority)
        tm.add_task(task)
        print("Task added.")

    elif choice == "2":
        tasks = tm.list_tasks()
        if not tasks:
            print("No tasks.")
        else:
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task.title} | {task.deadline} | {task.priority} | {task.status}")

    elif choice == "3":
        index = int(input("Enter task number to delete: ")) - 1
        tm.delete_task(index)
        print(" Task deleted.")

    elif choice == "4":
        print(" Exiting TaskForge.")
        break

    else:
        print(" Invalid choice. Try again.")
