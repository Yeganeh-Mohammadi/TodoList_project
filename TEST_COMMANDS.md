# Test Commands for TodoList CLI

## Step 1: Reset Database (Drop old tables and create new ones with Integer IDs)

```bash
python -m app.db.reset_db
```

**Expected output:**
```
Dropping existing tables...
Creating new tables with Integer IDs...
✓ Database reset successfully!
✓ Tables created with Integer autoincrement IDs starting from 1
```

---

## Step 2: Test Help Command

```bash
python main.py help
```

**Expected output:** List of all available commands

---

## Step 3: Create Projects

```bash
python main.py project create "Demo Project" "Demo description"
python main.py project create "Work Tasks" "Work related tasks"
python main.py project create "Personal" "Personal tasks"
```

**Expected output:**
```
Success: Project 'Demo Project' created successfully!
   ID: 1
   Description: Demo description
```

---

## Step 4: List All Projects

```bash
python main.py project list
```

**Expected output:** List of all projects with IDs starting from 1

---

## Step 5: Show Project Details

```bash
python main.py project show 1
```

**Expected output:** Project details with ID: 1

---

## Step 6: Create Tasks

```bash
python main.py task create "Overdue Task" 1 "This task is overdue" "2024-12-31 10:00"
python main.py task create "Future Task" 1 "This task is in the future" "2099-01-01 12:00"
python main.py task create "Task 3" 1 "Normal task"
python main.py task create "Work Task 1" 2 "Important work task"
```

**Expected output:**
```
Success: Task 'Overdue Task' created successfully!
   ID: 1
   Status: todo
   Deadline: 2024-12-31 10:00:00
```

---

## Step 7: List All Tasks

```bash
python main.py task list
```

**Expected output:** List of all tasks with IDs starting from 1

---

## Step 8: List Tasks by Project

```bash
python main.py task list 1
```

**Expected output:** List of tasks for project ID 1

---

## Step 9: Show Task Details

```bash
python main.py task show 1
```

**Expected output:** Task details with ID: 1

---

## Step 10: Update Task Status

```bash
python main.py task update-status 1 done
python main.py task update-status 2 doing
python main.py task update-status 3 todo
```

**Expected output:**
```
Success: Task 'Overdue Task' status changed to 'done'!
   Closed at: 2025-12-09 XX:XX:XX
```

---

## Step 11: Schedule Task (Update Deadline)

```bash
python main.py task schedule 2 "2099-12-31 23:59"
```

**Expected output:**
```
Success: Task 'Future Task' deadline set to '2099-12-31 23:59:00'!
```

---

## Step 12: Test Autoclose Overdue Tasks

```bash
python main.py tasks:autoclose-overdue
```

**Expected output:** List of overdue tasks that were automatically closed

---

## Step 13: Delete Task

```bash
python main.py task delete 3
```

**Expected output:**
```
Success: Task 'Task 3' deleted successfully!
```

---

## Step 14: Delete Project (Should also delete its tasks)

```bash
python main.py project delete 1
```

**Expected output:**
```
Deleting project 'Demo Project'...
   2 task(s) will also be automatically deleted.
Success: Project 'Demo Project' and 2 task(s) deleted successfully!
```

---

## Step 15: Verify Cascade Delete

```bash
python main.py task list
```

**Expected output:** Should show only tasks from remaining projects (project ID 2)

---

## Step 16: Show Remaining Project

```bash
python main.py project show 2
```

**Expected output:** Project details with its remaining tasks

---

## Step 17: Final Cleanup (Optional)

```bash
python main.py project delete 2
python main.py project delete 3
python main.py project list
```

**Expected output:** No projects found

---

## Notes:

- All IDs should start from 1 and increment sequentially
- When you delete a project, all its tasks should be automatically deleted (cascade delete)
- Task statuses: todo, doing, done
- Deadline format: YYYY-MM-DD or YYYY-MM-DD HH:MM

