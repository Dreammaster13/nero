"""
This is the app's primary engine
"""
import csv


class Core:
    """
    This class contains the core functionalities of the app
    """
    def __init__(self, filename):
        csv.register_dialect('nero', delimiter=',', lineterminator='\n')
        self.filename = filename

        file = open(self.filename, 'r')
        self.task_reader = csv.reader(file, 'nero')

        self.titles = [task[0] for task in self.task_reader]
        file.seek(0)
        self.deadlines = [task[1] for task in self.task_reader]

        file.close()

    def __len__(self):
        return len(self.titles)

    def __getitem__(self, idx):
        if idx > len(self.titles) - 1:
            raise IndexError("Index is out of bounds")
        elif idx < 0:
            raise IndexError("Index cannot be less than 0")

        return self.titles[idx]

    def __iter__(self):
        for i in range(len(self.titles)):
            yield self.titles[i]

    def __str__(self):
        try:
            max_ttl_len = len(max(self.titles, key=len))
            max_ddl_len = len(max(self.deadlines, key=len))
        except:
            max_ttl_len = max_ddl_len = 0

        res = "Title" + ' ' * (max_ttl_len - len("Title") + 22) + "Deadline"
        res += '\n' + '='*(max_ttl_len + max_ddl_len + 22) + '\n'

        for idx, task in enumerate(zip(self.titles, self.deadlines)):
            res += str(idx+1) + '.'
            res += ''.join(word.ljust(max_ttl_len + 20) for word in task)
            res += '\n'

        return res

    def get_titles(self):
        """Return the list of task titles"""
        return self.titles

    def get_deadlines(self):
        """Return the list of task deadlines"""
        return self.deadlines

    def add_task(self, title, deadline):
        """Add a new task"""
        file = open(self.filename, 'a')
        task_writer = csv.writer(file, 'nero')

        task_writer.writerow([title, deadline])
        self.titles.append(title)
        self.deadlines.append(deadline)

        file.close()

    def remove_task(self, idx):
        """Remove a task by the index"""
        file = open(self.filename, 'w')
        task_writer = csv.writer(file, 'nero')

        del self.titles[idx-1]
        del self.deadlines[idx-1]

        task_writer.writerows(zip(self.titles, self.deadlines))

        file.close()
