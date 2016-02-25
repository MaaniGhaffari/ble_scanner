#include <stdio.h>
#include <unistd.h> 

int main (int argc, char *argv[]) {
    if (argc < 2) {
        puts("Path to python script required.");
        return 1;
    }
    const char *python = "python";
    argv[0] = (char*)python;
    return execv("/usr/bin/python", argv);
}
