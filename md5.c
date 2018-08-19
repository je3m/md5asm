#include <stdint.h>
#include <stdio.h>

extern uint32_t* md5asm(int argc, char* filename);

int main(int argc, char const *argv[])
{

  uint32_t* buf = md5asm(argc, (char *) argv[1]);

  printf("%x %x %x %x\n", buf[0], buf[1], buf[2], buf[3]);

  return 0;
}