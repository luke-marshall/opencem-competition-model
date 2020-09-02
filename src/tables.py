from prettytable import PrettyTable

import re


class TableManager():
    def __init__(self):
        self.tables = {}
        self.field_names = {}

    def add_row(self, table_name, row):
        """Takes a table name and a list of items to go in a row. """
        self.tables[table_name] = [] if table_name not in self.tables else self.tables[table_name]
        self.tables[table_name].append(row)
    
    def set_field_names(self,table_name, field_names ):
        """Takes a table name and a list of field names."""
        self.field_names[table_name] = field_names

    def print_tables(self):
        """Pretty-prints all the tables to terminal."""
        for table_name in self.tables:
            pt = PrettyTable()
            pt.field_names = self.field_names[table_name] if table_name in self.field_names else []
            for row in self.tables[table_name]:
                pt.add_row(row)
            print("\n",table_name)
            print(pt)

    def export_tables_to_csv(self, csv_filename):
        """Puts all the tables in one big csv."""
        
        with open(csv_filename, 'w') as f:
            for table_name in self.tables:
                lines = [
                    "\n",
                    table_name,
                    "\n",
                    ', '.join(self.field_names[table_name]) if table_name in self.field_names else ""
                    "\n",
                    "\n",
                ]
                for row in self.tables[table_name]:
                    lines.append(', '.join([str(x) for x in row])) 
                    lines.append("\n")

                f.writelines(lines)