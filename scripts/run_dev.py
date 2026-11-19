"""Run the local dev servers and clean up the processes this run starts."""

from contextlib import ExitStack
import os
import shutil
import signal
import subprocess
import sys
from time import monotonic, sleep
from urllib.request import urlopen


def grobid_is_ready(url):
    try:
        with urlopen(f"{url}/api/isalive", timeout=2) as response:
            return response.read().strip() == b"true"
    except OSError:
        return False


def wait_for_grobid(cleanup, stopping):
    url = os.environ["GROBID_URL"].rstrip("/")
    if grobid_is_ready(url):
        print(f"GROBID is ready at {url}", flush=True)
        return

    quiet = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if not shutil.which("docker") or subprocess.run(["docker", "info"], **quiet).returncode:
        print("WARNING: Docker not available, running without GROBID", flush=True)
        return

    name = os.environ["GROBID_CONTAINER"]
    list_container = ["docker", "ps", "-q", "-f", f"name=^{name}$"]
    if not stopping() and not subprocess.check_output(list_container).strip():
        image = os.environ["GROBID_IMAGE"]
        if subprocess.run(["docker", "image", "inspect", image], **quiet).returncode:
            subprocess.run(["docker", "pull", image], check=True)
        if stopping():
            return
        print(f"Starting GROBID container {name}", flush=True)
        # Let Docker finish creating the container so its ID is available for cleanup.
        container_id = subprocess.check_output(
            ["docker", "run", "-d", "--rm", "--pull=never", "--name", name,
             "-p", "8070:8070", image],
            text=True,
            start_new_session=True,
        ).strip()
        cleanup.callback(stop_grobid, container_id)

    timeout = int(os.environ["GROBID_WAIT"])
    deadline = monotonic() + timeout
    print(f"Waiting for GROBID at {url}", flush=True)
    while not stopping():
        if grobid_is_ready(url):
            print(f"GROBID is ready at {url}", flush=True)
            return
        if not subprocess.check_output(list_container).strip():
            raise RuntimeError("GROBID container exited during startup")
        if monotonic() >= deadline:
            raise RuntimeError(f"GROBID was not ready after {timeout}s (see docker logs {name})")
        sleep(1)


def stop_grobid(container_id):
    print("Stopping GROBID", flush=True)
    subprocess.run(
        ["docker", "stop", container_id],
        stdout=subprocess.DEVNULL,
        start_new_session=True,
    )


def signal_group(process, signum):
    try:
        os.killpg(process.pid, signum)
    except ProcessLookupError:
        return False
    return True


def stop_servers(servers):
    for process in servers:
        signal_group(process, signal.SIGTERM)

    deadline = monotonic() + 10
    for process in servers:
        process.poll()
        while signal_group(process, 0):
            if monotonic() >= deadline:
                signal_group(process, signal.SIGKILL)
                break
            sleep(0.1)
            process.poll()
        process.wait()


def run_servers(make_command, stopping):
    servers = []
    try:
        for target in ("backend", "frontend"):
            if stopping():
                return 0
            servers.append(subprocess.Popen(
                [make_command, "--no-print-directory", target],
                start_new_session=True,
            ))

        while not stopping():
            for process in servers:
                status = process.poll()
                if status is not None:
                    return status if status >= 0 else 128 - status
            sleep(0.1)
        return 0
    finally:
        stop_servers(servers)


def main(make_command):
    interrupt = None

    def request_stop(signum, _frame):
        nonlocal interrupt
        interrupt = interrupt or signum

    def stopping():
        return interrupt is not None

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    status = 0
    try:
        with ExitStack() as cleanup:
            wait_for_grobid(cleanup, stopping)
            if not stopping():
                if make_command:
                    status = run_servers(make_command, stopping)
                else:
                    # A successful standalone `make grobid` keeps its container running.
                    cleanup.pop_all()
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        if not stopping():
            print(f"ERROR: {error}", file=sys.stderr)
        status = 1

    return 128 + interrupt if interrupt is not None else status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
