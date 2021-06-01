##########################################################################
#
# Program: hello_world_gas_solution_3
#
# Date: 05/28/2021
#
# Author: Travis Phillips
#
# Purpose: An updated hello world program safe for shellcode that is
#          reduced in size compared to previous versions.
#
# Compile: as --march=i386 --32 ./hello_world_gas_solution_3.s -o hello_world_gas_solution_3.o
#    Link: ld -m elf_i386 hello_world_gas_solution_3.o -o hello_world_gas_solution_3
#
##########################################################################
.global  _start                 # we must export the entry point to the
                                # ELF linker or loader. Conventionally,
                                # they recognize _start as their entry
                                # point but this can be overridden with
                                # ld -e "label_name" when linking.

.text                           # .text section declaration

_start:
    jmp my_string               # Jump to the my_string label.
payload:
    ######################################
    # syscall - write(1, msg, 14);
    ######################################
    push   $4
    pop    %eax                 # 4 = Syscall number for Write()

    push   $1                   # Push 1 to the stack.
    pop    %ebx                 # File Descriptor to write to
                                # In this case: STDOUT is 1

    pop    %ecx                 # Pop the string address pointer
                                # off the stack into ecx.

    push   $0x0e                # Push the length directly.
    pop    %edx                 # pop it into edx.

    int    $0x80                # Poke the kernel and tell it to run the
                                # write() call we set up

    ######################################
    # syscall - exit(bytes_printed);
    ######################################
    # exchange eax and ebx registers. This
    # instruction is only one byte!
    #
    # ebx currently has 1 for STDOUT. This
    # is also the syscall for exit().
    #
    # eax has the number of bytes written!
    # This will invoke exit with a status
    # code of the number of bytes written!
    ######################################
    xchg    %ebx,%eax           # Swap eax and ebx
    int     $0x80               # Poke kernel. This will end the program.

my_string:
    call   payload              # Call to the payload label. This will
                                # push the pointer to msg onto the stack
                                # as a return address.

msg:
    .ascii    "Hello, World!\n" # Declare a label "msg" which has
                                # our string we want to print.
