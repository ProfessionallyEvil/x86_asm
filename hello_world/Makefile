all: hello_world_c hello_world_nasm hello_world_gas

hello_world_nasm:
	@echo "\n\033[33;1mBuilding NASM Hello World\033[0m"
	nasm -f elf hello_world_nasm.asm
	ld -m elf_i386 hello_world_nasm.o -o hello_world_nasm

hello_world_c:
	@echo "\n\033[33;1mBuilding C Hello World\033[0m"
	gcc hello_world.c -o hello_world_c

hello_world_gas:
	@echo "\n\033[33;1mBuilding GAS Hello World\033[0m"
	as --march=i386 --32 ./hello_world_gas.s -o hello_world_gas.o
	ld -m elf_i386  hello_world_gas.o -o hello_world_gas

clean:
	@echo "\n\033[33;1mRemoving executables and object files\033[0m"
	rm -f hello_world_c
	rm -f hello_world_nasm hello_world_nasm.o
	rm -f hello_world_gas hello_world_gas.o

