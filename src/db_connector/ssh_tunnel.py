import os
import signal
import subprocess


class SSHTunnel:
    def __init__(self, ssh_cmd: str) -> None:
        self.ssh_cmd = ssh_cmd

    def main(self):
        existing_ssh_tunnels = self._get_running_ssh_pids()

        if len(existing_ssh_tunnels) >= 1:
            self._terminate_processes_by_pids(existing_ssh_tunnels)

        self.open_ssh_tunnel()

    def open_ssh_tunnel(self):
        exit_status = os.system(self.ssh_cmd + "&")
        if exit_status != 0:
            raise Exception("Error: could not open ssh tunnel.")
        else:
            print("SSH Connection established.")

    def _get_running_ssh_pids(self) -> list[str]:
        ps = subprocess.Popen(("ps", "-A"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("grep", "ssh"), stdin=ps.stdout)
        ps.wait()

        s = output.decode("utf-8")

        pids = []
        for line in s.split("\n"):
            if self.ssh_cmd in line:
                pid = line[:5]
                pids.append(pid)

        return pids

    @staticmethod
    def _terminate_processes_by_pids(pids: list[str]):
        for pid in pids:
            print(f"Terminating existing ssh process with pid {pid}")
            os.kill(int(pid), signal.SIGTERM)


if __name__ == "__main__":
    pass
