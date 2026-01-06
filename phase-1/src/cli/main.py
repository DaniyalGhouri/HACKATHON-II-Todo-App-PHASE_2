import sys
from src.cli.commands import CommandHandler

def print_menu():
    print("\n--- Todo In-Memory Console App ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Mark Task Incomplete")
    print("7. Exit")
    print("----------------------------------")

def get_int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    handler = CommandHandler()

    while True:
        print_menu()
        choice = input("Select an option (1-7): ").strip()

        try:
            if choice == "1":
                description = input("Enter task description: ").strip()
                handler.handle_add(description)
            
            elif choice == "2":
                handler.handle_list()
            
            elif choice == "3":
                task_id = get_int_input("Enter task ID to update: ")
                description = input("Enter new description: ").strip()
                handler.handle_update(task_id, description)
            
            elif choice == "4":
                task_id = get_int_input("Enter task ID to delete: ")
                handler.handle_delete(task_id)
            
            elif choice == "5":
                task_id = get_int_input("Enter task ID to mark complete: ")
                handler.handle_complete(task_id)
            
            elif choice == "6":
                task_id = get_int_input("Enter task ID to mark incomplete: ")
                handler.handle_incomplete(task_id)
            
            elif choice == "7":
                print("Exiting application. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please select 1-7.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()