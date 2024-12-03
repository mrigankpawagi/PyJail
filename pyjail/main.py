import os
import shutil
import venv
import pickle
import pwd
import random

class Jail:
    """
    This class creates and manages a chroot jail.
    """
    
    def __init__(self, path=os.path.join(os.getcwd(), "jail"), clear_before_create=False):
        self.path = path
        self.jail_user = "nobody-{}".format(str(random.random())[2:])

        if clear_before_create:
            shutil.rmtree(self.path, ignore_errors=True)

        self.create_nobody_user()
        os.makedirs(self.path, exist_ok=True)

    def create_nobody_user(self):
        """
        Creates an unprivileged user to run the jail.
        """
        os.system(f"sudo useradd -M -N -r -s /bin/false {self.jail_user}")

    def execute(self, func, *args, **kwargs):
        """
        Execute a function securely inside the chroot jail.
        """
        # pipe for communication between parent and child processes
        read_pipe, write_pipe = os.pipe()
        read_pipe_err, write_pipe_err = os.pipe()

        def _run_in_jail():
            """
            This function is executed inside the chroot jail to run the given function.
            """
            jail_gid = pwd.getpwnam(self.jail_user).pw_gid
            jail_uid = pwd.getpwnam(self.jail_user).pw_uid
            
            os.chroot(self.path)
            os.chdir("/")
            os.setgid(jail_gid)
            os.setuid(jail_uid)

            try:
                return_value = func(*args, **kwargs)
                os.write(write_pipe, pickle.dumps(return_value))
                os.write(write_pipe_err, b"")
            except Exception as e:
                os.write(write_pipe_err, pickle.dumps(e))
            finally:
                os.close(write_pipe)
                os.close(write_pipe_err)

        # Fork a process that starts from the jail
        pid = os.fork()
        if pid == 0:
            _run_in_jail()
            quit()
        else:
            os.waitpid(pid, 0)
            os.close(write_pipe)
            os.close(write_pipe_err)
            
            # check if there was an exception in the child process
            err = open(read_pipe_err, "rb").read()
            if err:
                print("An exception occurred in the child process.")
                raise pickle.loads(err)
            else:
                return_value = pickle.loads(open(read_pipe, "rb").read())
                return return_value

    def destroy(self):
        """
        Destroy the chroot jail and associated resources.
        """
        shutil.rmtree(self.path, ignore_errors=True)
        os.system(f"sudo userdel {self.jail_user}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.destroy()
