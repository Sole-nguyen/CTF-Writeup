#include <stdio.h>
#include <dlfcn.h>

int main() {
    void *handle;
    void (*enter_level)(void);
    void (*leave_level)(void);
    char *error;

    // Load the shared library
    handle = dlopen("./level_2.so", RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "Error loading library: %s\n", dlerror());
        return 1;
    }

    // Load the enter_level function
    enter_level = dlsym(handle, "enter_level");
    error = dlerror();
    if (error != NULL) {
        fprintf(stderr, "Error loading enter_level: %s\n", error);
        return 1;
    }

    printf("Calling enter_level()...\n");
    enter_level();

    // Load the leave_level function
    leave_level = dlsym(handle, "leave_level");
    error = dlerror();
    if (error != NULL) {
        fprintf(stderr, "Error loading leave_level: %s\n", error);
        return 1;
    }

    printf("Calling leave_level()...\n");
    leave_level();

    dlclose(handle);
    return 0;
}
