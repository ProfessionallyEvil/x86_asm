/****************************************************
*
* Program: hello_world
*
* Date: 04/20/2021
*
* Author: Travis Phillips
*
* Purpose: A simple hello world written in C that
*          mimics what we are going to write in x86
*          ASM using write and exit calls.
*
* Compile: gcc -m32 hello_world.c -o hello_world_c
*
****************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char *msg = " [*] Hello World!\n";

int main() {
    // Write the message to STDIN.
    write(1, msg, strlen(msg));

    // Exit with status code 0;
    exit(0);
}
