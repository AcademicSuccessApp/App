from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    @abstractmethod
    def login(self):
        pass
    
    def logout(self):
        pass

class Student(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.student_id = None
        self.gpa = None
        self.attendance = None
        self.credits = None
    
    def login(self):
        # Implement actual login logic here
        return True if self.username and self.password else False

class Teacher(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.teacher_id = None
    
    def login(self):
        # Implement actual login logic here
        return True if self.username and self.password else False 