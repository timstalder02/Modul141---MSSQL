

def execute_sql_statements(usedList):
    for command_to_execute in usedList:
        cursor.execute(command_to_execute)

def delete_files(usedList):
    for delete_file in delete_files:
        if os.path.exists(delete_file):
            os.remove(delete_file)