all: x86_shellcode_tester


x86_shellcode_tester:
	@echo "\n\033[33;1mBuilding X86 Shellcode Tester\033[0m"
	gcc -m32 x86_shellcode_tester.c -o x86_shellcode_tester

clean:
	@echo "\n\033[33;1mRemoving executables and object files\033[0m"
	rm -f x86_shellcode_tester
