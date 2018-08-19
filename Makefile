all: md5.asm
	nasm -felf64 -g md5.asm
	gcc -o md5_c.o -c -g md5.c
	gcc -o md5 -g md5.o md5_c.o

clean:
	rm md5.o
	rm md5_c.o
	rm md5
