##########################################################################
#
# Program: hello_world_gas_solution_2
#
# Date: 05/28/2021
#
# Author: Travis Phillips
#
# Purpose: An updated hello world program in x86 assembly for GAS that
#          implements solution 1 to make the string address dynamic, but
#          also fixes the null byte issues.
#
# Compile: as --march=i386 --32 ./hello_world_gas_solution_2.s -o hello_world_gas_solution_2.o
#    Link: ld -m elf_i386 hello_world_gas_solution_2.o -o hello_world_gas_solution_2
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
    # syscall - write(1, msg, len);
    ######################################
    xor    %eax,%eax            # Zero out eax.
    xor    %ebx,%ebx            # Zero out ebx.
    xor    %edx,%edx            # Zero out edx.
    mov    $4,%al               # 4 = Syscall number for Write()

    mov    $1,%bl               # File Descriptor to write to
                                # In this case: STDOUT is 1

    pop    %ecx                 # Pop the string address pointer
                                # off the stack into ecx.

    mov    $len,%dl             # The length of string to print
                                # which is 14 characters

    int    $0x80                # Poke the kernel and tell it to run the
                                # write() call we set up

    ######################################
    # syscall - exit(0);
    ######################################
    # Note: If your message was more than
    # 255 characters, you will need to
    # either zero out eax again via xor,
    # or mov %ebx,%eax.
    ######################################
    mov    $1,%al               # 1 = Syscall for Exit()
    xor    %ebx,%ebx            # The status code we want to provide.
    int    $0x80                # Poke kernel. This will end the program.

my_string:
    call   payload              # Call to the payload label. This will
                                # push the pointer to msg onto the stack
                                # as a return address.

msg:
    .ascii    "Hello, World!\n" # Declare a label "msg" which has
                                # our string we want to print.

    len = . - msg               # "len" will calculate the current
                                # offset minus the "msg" offset.
                                # this should give us the size of
                                # "msg".
