from subprocess import Popen, PIPE
import shutil
import os
import glob


def update_build_version_no():
    with open('.env_package', 'r') as fl:
        version = fl.readlines()[0].replace('package_version=', '')
        major_version = version.split('.')[0]
        minor_version = version.split('.')[1]
        build_no = str(int(version.split('.')[2]) + 1)
        new_version = f'{major_version}.{minor_version}.{build_no}'

    with open('.env_package', 'w') as fl:
        fl.write(f'package_version={new_version}')


def main():
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    if os.path.exists('build'):
        shutil.rmtree('build')

    files = glob.glob('zeppos_*.egg-info')
    for file in files:
        shutil.rmtree(file)

    p = Popen(['pytest'], stdout=PIPE)
    out, err = p.communicate()

    out_array = out.decode("utf-8") .split('\r\n')

    if "passed" in out_array[len(out_array)-2]:
        print("Test Passed")

        update_build_version_no()

        p = Popen(['pipenv', 'run', 'python', 'setup.py', 'sdist', 'bdist_wheel'])
        p.communicate()

        p = Popen(['pipenv', 'run', 'python', '-m', 'twine', 'upload', '--skip-existing', '--repository', 'testpypi', 'dist/*'])
        p.communicate()
    else:
        print("Test Failed")
        for line in out_array:
            print(line)


if __name__ == '__main__':
    main()

