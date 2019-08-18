import subprocess
import os


def compilation():
    p = subprocess.Popen("", stdin=subprocess.PIPE, shell=True)
    pipe = p.communicate()
    print(pipe[1].decode('utf-8').strip())

    os.chdir(path)   # path = cwd + '/data/usersCode/' + username + '/que' + str(qn) + '/'
    f = open("solution" + str(qn) + ".cpp", "r")
    s = subprocess.Popen('g++ f.cpp -o out:./out', stdout=subprocess.PIPE, shell=True).communicate()[0]
    print(s.decode('utf-8'))

    if s.returncode == 0:
        testcase()

#def testcase():
    # compare(path1=, path2=, i)


def compare(path, path1, i):  # path1 = required output
    file1 = subprocess.Popen('{}/out'.format(path), stdout=subprocess.PIPE, shell=True).communicate()[0].decode(
        'utf-8')
    file2 = subprocess.Popen('{}/output{}'.format(path1, i), stdout=subprocess.PIPE, shell=True).communicate()[0]
    for line1 in file1.strip():
        for line2 in file2.strip():
            if line1 != line2:
                return -1


if __name__ == '__main__':
    compilation()
    compare()
    testcase()
