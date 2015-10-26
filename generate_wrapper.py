import os

cpp_code = """
#include <iostream>
#include <iomanip>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>

using namespace std;

int main(int argc, const char* argv[]) {
    string python_executable = "/usr/bin/python";
    string main_file_path = "%(python_main)s";
    if (argc == 2){
        cerr<<"Usage: "<<argv[0]<<" [--python <python executable>]"<<endl;
        return 0;
    }
    if (argc == 3){
        // Python path is given
        string arg1 = argv[1];
        if (arg1 != "--python"){
            cerr<<"Usage: "<<argv[0]<<" [--python <python executable>]"<<endl;
            return 0;
        }
        python_executable = argv[2];
    }

    int script_return;
    unsigned int uid = getuid();
    string uname = getpwuid(uid)->pw_name;

    char buffer[256];

    setuid(0);    //become root
    sprintf(buffer, "%%s %%s %%s", python_executable.c_str(), main_file_path.c_str(), uname.c_str());
    script_return = system(buffer);
    return script_return %% 10;
}
"""


def get_abs_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

python_main = get_abs_path('printmain.py')

cpp_code = cpp_code % {'python_main': python_main}

output_file = get_abs_path('generated_wrapper.cpp')

with open(output_file, 'w') as f:
    f.write(cpp_code)
