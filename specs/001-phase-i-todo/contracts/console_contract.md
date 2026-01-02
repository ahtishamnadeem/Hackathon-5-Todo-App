# Console Interface Contract

Since Phase I is a console app, "contracts" define the expected input/output for the CLI.

## Menu Options
1. Add Todo: Prompt for title -> create todo
2. View Todos: Display list of (ID, status, title)
3. Update Todo: Prompt for ID -> prompt for new title -> update
4. Delete Todo: Prompt for ID -> delete
5. Mark Complete: Prompt for ID -> toggle status
6. Exit: Close application

## Output Format
```text
ID  Status      Title
--  ----------  -----
1   [Pending]   Buy milk
2   [Done]      Write code
```
