class SubmissionResult:
    def __init__(self, action, full_id, status):
        self._action = action
        self._full_id = full_id
        self._status = status

    @property
    def action(self):
        return self._action

    @property
    def full_id(self):
        return self._full_id

    @property
    def status(self):
        return self._status

    def __str__(self):
        return (f"<Submission Result - "
                f"Action: {self.action} - "
                f"Full ID: {self.full_id} - "
                f"Status: {self.status}>")

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return {'action': self.action, 'full_id': self.full_id,
                'status': self.status}
