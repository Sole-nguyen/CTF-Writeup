// gcc -no-pie -Wl,-z,relro -fstack-protector-all -o chal src.c
#include <stdio.h>
#include <stdlib.h>

#define SIZE 0x10

char *msg = "Update Complete";
int values[SIZE];
int idx, i;

void handle_error() {
  system("echo ERROR OCCURRED");
  exit(1);
}

void edit() {
  while (1) {
    printf("index? > ");
    if (scanf("%d", &idx) != 1) {
      handle_error();
    }
    if (idx == -1) {
      break;
    }
    printf("value? > ");
    if (scanf("%d", &values[idx]) != 1) {
      handle_error();
    }
  }

  puts(msg);
  printf("Array: ");
  for (i = 0; i < SIZE; i++) {
    printf("%d ", values[i]);
  }
  printf("\n");
}

int main() {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  edit();
  return 0;
}
