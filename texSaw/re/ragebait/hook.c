#define _GNU_SOURCE
#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>

static void print_arg(const char *s) {
    if (!s) { fputs("<null>", stderr); return; }
    fputc('"', stderr);
    for (const unsigned char *p = (const unsigned char*)s; *p; ++p) {
        unsigned char c = *p;
        if (c == '"' || c == '\\') { fputc('\\', stderr); fputc(c, stderr); }
        else if (c >= 32 && c < 127) fputc(c, stderr);
        else fprintf(stderr, "\\x%02x", c);
    }
    fputc('"', stderr);
}

int execve(const char *pathname, char *const argv[], char *const envp[]) {
    (void)envp;
    fputs("[HOOK] execve path=", stderr);
    print_arg(pathname);
    if (argv) {
        for (int i = 0; i < 10; i++) {
            if (!argv[i]) { fprintf(stderr, " argv[%d]=<null>", i); break; }
            fprintf(stderr, " argv[%d]=", i);
            print_arg(argv[i]);
        }
    }
    fputc('\n', stderr);
    errno = ENOENT;
    return -1;
}

int usleep(useconds_t usec) { (void)usec; return 0; }
int nanosleep(const struct timespec *req, struct timespec *rem) { (void)req; (void)rem; return 0; }
