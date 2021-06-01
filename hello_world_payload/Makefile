all: hello_world_gas hello_world_gas_solution_1 hello_world_gas_solution_2 hello_world_gas_solution_3


hello_world_gas:
	@echo "\n\033[33;1mBuilding Original GAS Hello World\033[0m"
	as --march=i386 --32 ./hello_world_gas.s -o hello_world_gas.o
	ld -m elf_i386  hello_world_gas.o -o hello_world_gas

hello_world_gas_solution_1:
	@echo "\n\033[33;1mBuilding Solution 1 GAS Hello World\033[0m"
	as --march=i386 --32 ./hello_world_gas_solution_1.s -o hello_world_gas_solution_1.o
	ld -m elf_i386  hello_world_gas_solution_1.o -o hello_world_gas_solution_1

hello_world_gas_solution_2:
	@echo "\n\033[33;1mBuilding Solution 2 GAS Hello World\033[0m"
	as --march=i386 --32 ./hello_world_gas_solution_2.s -o hello_world_gas_solution_2.o
	ld -m elf_i386  hello_world_gas_solution_2.o -o hello_world_gas_solution_2

hello_world_gas_solution_3:
	@echo "\n\033[33;1mBuilding Solution 3 GAS Hello World\033[0m"
	as --march=i386 --32 ./hello_world_gas_solution_3.s -o hello_world_gas_solution_3.o
	ld -m elf_i386  hello_world_gas_solution_3.o -o hello_world_gas_solution_3

clean:
	@echo "\n\033[33;1mRemoving executables and object files\033[0m"
	rm -f hello_world_gas hello_world_gas.o
	rm -f hello_world_gas_solution_1 hello_world_gas_solution_1.o
	rm -f hello_world_gas_solution_2 hello_world_gas_solution_2.o
	rm -f hello_world_gas_solution_3 hello_world_gas_solution_3.o

