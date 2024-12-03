import os
import venv

class Jail:
    """
    This is the primary class that will be used to create a chroot jail.
    """
    
    def __init__(self, path=os.getcwd()):
        self.path = path
        
    def create_venv(self):
        """
        Create a virtual environment inside the jail.
        """
        venv.create(self.path)
