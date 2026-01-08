from typing import List, Dict, TypedDict


class ErrorRecordDict(TypedDict):
    task: str
    mistake: str
    count: int


class ErrorRecord:
    def __init__(self, task: str, mistake: str) -> None:
        self.task = task
        self.mistake = mistake
        self.count = 1


class ErrorMemory:
    def __init__(self) -> None:
        self.records: List[ErrorRecord] = []

    def add(self, task: str, mistake: str) -> None:
        for record in self.records:
            if record.task == task and record.mistake == mistake:
                record.count += 1
                return

        self.records.append(ErrorRecord(task, mistake))

    def all(self) -> List[ErrorRecordDict]:
        return [
            {
                "task": record.task,
                "mistake": record.mistake,
                "count": record.count
            }
            for record in self.records
        ]
