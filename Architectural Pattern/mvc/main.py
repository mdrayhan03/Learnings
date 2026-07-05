class TaskModel:
    def __init__(self, task_id: int, title: str):
        self.id: int = task_id
        self.title: str = title
        self.complete: bool = False

class TaskTitleValidator:
    @staticmethod
    def title_validate(task: TaskModel) -> bool:
        if len(task.title.strip()) == 0:
            raise ValueError("[ERROR] Task title can't be empty!")
        return True

class TaskRepository:
    def __init__(self):
        self._tasks: list[TaskModel] = []
    
    def add_task(self, task_id: int, title: str) -> bool:
        task = TaskModel(task_id, title)
        try:
            if TaskTitleValidator.title_validate(task):
                self._tasks.append(task)
                return True
        except ValueError as ve:
            print(ve)
            return False
        return False
    
    def complete_task(self, task_id: int) -> bool:
        for task in self._tasks:
            if task.id == task_id:
                task.complete = True
                return True
        return False
    
    def get_all_tasks(self) -> list[TaskModel]:
        return self._tasks

############
# V -> View (Completely Decoupled & Pure)
############
class TaskView:
    # Removed repository injection. View now only handles data transformation.
    def render(self, tasks: list[TaskModel], alert_message: str = "") -> str:
        # A mock HTML Template structure
        html_template = """
        <html>
            <head><title>Task Dashboard</title></head>
            <body>
                {message_banner}
                <h1>Task List</h1>
                <ul>
        {task_items}
                </ul>
            </body>
        </html>
        """
        
        # Build list items
        task_items_str = ""
        for task in tasks:
            status = "DONE" if task.complete else "PENDING"
            task_items_str += f"            <li>[{status}] {task.id}. {task.title}</li>\n"
        
        # Build dynamic alert banner if exists
        message_banner = f"<div class='alert'>{alert_message}</div>" if alert_message else ""
        
        # Merge data directly into template
        return html_template.format(message_banner=message_banner, task_items=task_items_str).strip()
    
##################
# C -> Controller
##################
class TaskController:
    def __init__(self, task_view: TaskView, task_repo: TaskRepository):
        self.task_view: TaskView = task_view
        self.task_repo: TaskRepository = task_repo

    def handle_view_tasks(self, alert_message: str = "") -> str:
        # 1. Grab data from the Model/Repository layer
        all_tasks = self.task_repo.get_all_tasks()
        # 2. Inject data into View and return compiled output
        return self.task_view.render(all_tasks, alert_message)

    def handle_add_task(self, user_input_title: str) -> str:
        next_id = len(self.task_repo.get_all_tasks()) + 1
        success = self.task_repo.add_task(next_id, user_input_title)
        
        if success:
            msg = f"Task {next_id} added successfully."
        else:
            msg = f"Task registration failed due to validation error."
            
        # Standard MVC behavior: Re-render dashboard view containing the new status alert
        return self.handle_view_tasks(alert_message=msg)

#############
# Simulation
#############
if __name__ == "__main__":
    # Setup MVC components
    repo = TaskRepository()
    view = TaskView()
    controller = TaskController(view, repo)
    
    print("--- 1. Viewing Initial Empty Dashboard ---")
    print(controller.handle_view_tasks())
    print("-" * 60)
    
    print("\n--- 2. Executing Add Task Form Action ---")
    response_html = controller.handle_add_task("Learn Model-View-Presenter Pattern")
    print(response_html)
    print("-" * 60)

    print("\n--- 3. Executing Invalid Task Form Action ---")
    error_html = controller.handle_add_task("   ")  # Will trigger validator error
    print(error_html)