import utils.file
import subprocess
import sys
import typing


def run_module(name: str, args: list[str] = []) -> bool:
    return subprocess.run([sys.executable, '-m', name, *args]).returncode == 0


def pip_install(name: str) -> bool:
    return run_module('pip', ['install', name])


def print_desc(desc: str) -> None:
    print(desc, end='... ')


def silent_action(dest: str, func: typing.Callable[[], None]) -> None:
    print(f"==> {desc}")
    func()


def install_requirements() -> None:
    print_desc("Ensurepip")
    print('OK' if run_module('ensurepip') else 'failed')

    with open('requirements.txt') as reqs:
        for req in reqs:
            req = req.strip()
            print_desc(f"Installing {req}")
            print('OK' if pip_install(req) else 'failed')


def create_log():
    print_desc('Creating log folder')
    print('done!' if utils.file.create_dir('log') else 'already exist')


def create_user():
    print_desc('Creating user database')
    # TODO alternative user database....
    print('done!' if utils.file.create_dir('user') else 'already exist')


def create_config():
    print_desc('Configurating AlterPy')
    # TODO
    utils.file.create_dir('config')
    print("check /config_example folder")


def simple_setup():
    create_log()
    create_user()
    create_config()



print("==> requirements")
install_requirements()

print("==> configurating")
simple_setup()

