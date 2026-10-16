#!/usr/bin/env python3
"""Start/stop this checkout's independent RYLAY development services."""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.local' / 'dev-services.json'
SERVICES = [('api', 'backend', 8000, ['php', 'artisan', 'serve', '--host=127.0.0.1', '--port=8000']),
            ('admin', 'frontend', 5173, ['npm', 'run', 'dev']),
            ('app', 'app', 5174, ['npm', 'run', 'dev'])]


def listening(port):
    for host in ('127.0.0.1', '::1'):
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return True
        except OSError:
            pass
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['start', 'stop', 'status'])
    action = parser.parse_args().action
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    if action == 'status':
        for name, _, port, _ in SERVICES:
            print(f'{name}: {"listening" if listening(port) else "stopped"} (port {port})')
        return
    if action == 'stop':
        # Only stop process groups recorded by this launcher; never kill by port.
        for item in state.values():
            try:
                result = subprocess.run(['ps', '-p', str(item['pid']), '-o', 'lstart='], capture_output=True, text=True)
                if result.stdout.strip() and result.stdout.strip() == item.get('started'):
                    os.killpg(item['pid'], signal.SIGTERM)
            except ProcessLookupError:
                pass
        STATE.unlink(missing_ok=True)
        return
    if not (ROOT / 'backend/.env').exists():
        raise SystemExit('Create backend/.env and initialize its NEW database first; see README.md.')
    for directory in ['backend/vendor', 'frontend/node_modules', 'app/node_modules']:
        if not (ROOT / directory).is_dir():
            raise SystemExit(f'Missing {directory}; install dependencies first.')
    if any(listening(port) for _, _, port, _ in SERVICES):
        raise SystemExit('A requested port is occupied. Use status; existing processes were left untouched.')
    ROOT.joinpath('.local').mkdir(exist_ok=True)
    cluster = ROOT / '.local/postgres/data'
    if cluster.exists():
        pg_ctl = shutil.which('pg_ctl') or '/opt/homebrew/opt/postgresql@18/bin/pg_ctl'
        if subprocess.run([pg_ctl, '-D', str(cluster), 'status'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
            subprocess.run([pg_ctl, '-D', str(cluster), '-l', str(ROOT / '.local/postgres/server.log'), '-o', '-h 127.0.0.1 -p 55435', 'start'], check=True)
    for name, directory, port, command in SERVICES:
        with (ROOT / f'.local/{name}.log').open('ab') as log:
            process = subprocess.Popen(command, cwd=ROOT / directory, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
        time.sleep(0.1)
        started = subprocess.run(['ps', '-p', str(process.pid), '-o', 'lstart='], capture_output=True, text=True).stdout.strip()
        state[name] = {'pid': process.pid, 'started': started}
        STATE.write_text(json.dumps(state, indent=2))
    for _ in range(50):
        if all(listening(port) for _, _, port, _ in SERVICES):
            print('RYLAY Admin: http://localhost:5173/\nRYLAY App: http://127.0.0.1:5174/')
            return
        time.sleep(0.1)
    raise SystemExit('Some services did not start; inspect .local/*.log and run status.')


if __name__ == '__main__':
    main()
