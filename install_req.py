from pip._internal import main as pip_main

def install_requirements(requirements_file):
    with open(requirements_file) as f:
        requirements = f.read().splitlines()
    pip_main(['install', '-r', requirements_file])

if __name__ == '__main__':
    install_requirements('requirements.txt')
