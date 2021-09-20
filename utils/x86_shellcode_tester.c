/***********************************************************************
* 
* Program: x86_shellcode_tester.c
*
* Date: 08/06/2021
*
* Author: Travis Phillips
*
* Purpose: This code is used to provide a C template to paste shellcode
*          into and be able to run it live from within an ELF binary's
*          char buffer. This allows you to create a buffer with the
*          shellcode globally and this program will mark it as RWX using
*          mprotect() and then finally jump into.
*
* Compile: gcc -m32 x86_shellcode_tester.c -o x86_shellcode_tester
*
***********************************************************************/
#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

/////////////////////////////////////////////////////
//  source file: hello_world_gas_solution_3.s
// payload size: 36
/////////////////////////////////////////////////////
char payload[] = "\xeb\x0f\x6a\x04\x58\x6a\x01\x5b\x59\x6a\x0e\x5a\xcd\x80\x93\xcd"
                 "\x80\xe8\xec\xff\xff\xff\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72"
                 "\x6c\x64\x21\x0a";

int main() {
    // Print the banner.
    puts("\n\t\033[33;1m---===[ Shellcode Tester Stub v1.0 ]===---\033[0m\n");
    
    // Print the size of the shellcode.
    printf(" [\033[34;1m*\033[0m] Shellcode Size:  %d\n", sizeof(payload)-1);

    // Create a function pointer to the shellcode and
    // display it to the user.
    void (*payload_ptr)() =  (void(*)())&payload;
    printf(" [\033[34;1m*\033[0m] Shellcode Address: 0x%08x\n", payload_ptr);

    // Calculate the address to the start of the page for the
    // the shellcode.
    void *page_offset = (void *)((int)payload_ptr & ~(getpagesize()-1));
    printf(" [\033[34;1m*\033[0m] Shellcode page: 0x%08x\n", page_offset);

    // Use mprotect to mark that page as RWX.
    mprotect(page_offset, getpagesize(), PROT_READ|PROT_WRITE|PROT_EXEC);

    // Finally, use our function pointer to jump into our payload.
    puts("\n\033[33;1m---------[ Begin Shellcode Execution ]---------\033[0m");
    payload_ptr();

    // We likely won't get here, but might as well include it just in case.
    puts("\033[33;1m---------[  End Shellcode Execution  ]---------\033[0m");
    return 0;
}
