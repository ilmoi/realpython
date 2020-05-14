class ProductivityTracker(object):
    def track(self, employees, hours):
        print('---------------------')
        print('tracking productivity')
        for emp in employees:
            emp.work(hours)
        print('---------------------')
