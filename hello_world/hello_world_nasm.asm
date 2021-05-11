;***************************************************************
;
; Program: hello_world_nasm
;
; Date: 04/20/2021
;
; Author: Travis Phillips
;
; Purpose: A simple hello world program in x86 assembly for
;          NASM
;
; Compile: nasm -f elf hello_world_nasm.asm
;    Link: ld -m elf_i386 hello_world_nasm.o -o hello_world_nasm
;
;***************************************************************
global _start     ; global is used to export the _start label.
                  ; This will be the entry point to the program.

   ; The data segment of our program.
section .data
   msg: db "Hello, World!",0xa ; Declare a label "msg" which has
                               ; our string we want to print.
                               ; for reference: 0xa = "\n"

   len: equ $-msg              ; "len" will calculate the current
                               ; offset minus the "msg" offset.
                               ; this should give us the size of
                               ; "msg".

   ; The .text segement of our program, counter-intutively, this
   ; is where we store our executable code.
section .text
_start:
   ;######################################
   ; syscall - write(1, msg, len);
   ;######################################
   mov eax, 4     ; 4 = Syscall number for Write()

   mov ebx, 1     ; File Descriptor to write to
                  ; In this case: STDOUT is 1

   mov ecx, msg   ; String to write. A pointer to
                  ; the variable 'msg'

   mov edx, len   ; The length of string to print
                  ; which is 14 characters

   int 0x80       ; Poke the kernel and tell it to run the
                  ; write() call we set up

   ;######################################
   ; syscall - exit(0);
   ;######################################
   mov al, 1      ; Syscall for Exit()
   mov ebx, 0     ; The status code we want to provide.
   int 0x80       ; Poke kernel. This will end the program.
