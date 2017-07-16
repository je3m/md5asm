section .text
global _start

_start:
  push rbp
  mov rbp, rsp

  ; print out greeting
  mov rax, 1
  mov rdi, 1
  mov rsi, msg
  mov rdx, len
  syscall

  ; check argc
  mov r8, [rbp+8]
  cmp r8, 2
  jne bad_argc

  ; get file name from argv[1]
  mov rsi, [rbp+24]

  mov rax, 1
  call strlen
  syscall



  ; exit gracefully
  mov eax, 60
  xor rdi, rdi
  syscall


strlen: ; rsi -> rdx
  push rbp
  mov rbp, rsp
  lea rdx, [rsi - 1]
  _loop:
    inc rdx
    mov cl, [rdx]
    cmp cl, 0
    jne _loop
  sub rdx, rsi
  leave
  ret

bad_argc:
  mov rax, 1
  mov rdi, 1
  mov rsi, badargc
  mov rdx, badargclen
  syscall

  mov eax, 60
  mov rdi, 1
  syscall


section .data
  msg           db 'fap swag', 0xa
  len           equ $ - msg
  badargc       db 'invalid number of arguments', 0xa
  badargclen    equ $ - badargc

  K             dd 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee
                dd 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501
                dd 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be
                dd 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821
                dd 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa
                dd 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8
                dd 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed
                dd 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a
                dd 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c
                dd 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70
                dd 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05
                dd 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665
                dd 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039
                dd 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1
                dd 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1
                dd 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
