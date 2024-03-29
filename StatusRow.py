class StatusRow:
    def __init__(self, status_row = {"iter_num": 0, "action": "Adding body to string", "status": None, "ID": None}):
        vars(self)['status_row'] = status_row

    def __setattr__(self, attr, value):
        super(StatusRow, self).__setattr__(attr, value)
        print(self)

    def __str__(self):
        return "status_row"
        # return '| {:^9}| {:<22}| {:<15}| {}'.format(*self.status_row.values())
