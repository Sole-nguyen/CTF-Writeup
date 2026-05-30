import ctypes
import sys
import os

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

PyByteArray_AsString = ctypes.pythonapi.PyByteArray_AsString
PyByteArray_AsString.argtypes = [ctypes.py_object]
PyByteArray_AsString.restype = ctypes.c_void_p

class Buffer:
    def __init__(self, size):
        self.data = bytearray(size)
        self.ptr = PyByteArray_AsString(self.data)
        self.size = size

    def resize(self, new_size):
        if new_size > self.size:
            self.data.extend(b'\x00' * (new_size - self.size))
        else:
            self.data = self.data[:new_size]

        self.size = new_size

    def write(self, offset, value):
        if 0 <= offset < self.size:
            try:
                target = (ctypes.c_char * 1).from_address(self.ptr + offset)
                target[0] = int(value).to_bytes(1, 'little')
            except ValueError:
                pass
            except Exception:
                pass
        else:
            print("Offset out of bounds")

    def read(self, offset):
        if 0 <= offset < self.size:
            try:
                target = (ctypes.c_char * 1).from_address(self.ptr + offset)
                return target[0]
            except Exception:
                return b'\x00'
        return b''

    def addr(self):
        return self.ptr

buffers = []
vault = []

def main():
    print("Welcome to the Snake Manager.")
    print("We optimize for speed by caching poisons!")

    while True:
        print("\n1. Prepare")
        print("2. Grow")
        print("3. Write")
        print("4. Read")
        print("5. Reveal")
        print("6. Store")
        print("7. Retrieve")
        print("8. Exit")
        try:
            choice = input("Choice: ").strip()

            if choice == '1':
                try:
                    line = input("Size: ")
                    if not line: continue
                    size = int(line)
                    buffers.append(Buffer(size))
                    print(f"Prepared {len(buffers)-1}")
                except ValueError:
                    print("Invalid size")

            elif choice == '2':
                try:
                    idx = int(input("Index: "))
                    new_size = int(input("New Size: "))
                    if 0 <= idx < len(buffers):
                        buffers[idx].resize(new_size)
                        print("Grown.")
                except ValueError:
                    print("Invalid input")

            elif choice == '3':
                try:
                    idx = int(input("Index: "))
                    offset = int(input("Offset: "))
                    val = int(input("Value (byte): "))
                    if 0 <= idx < len(buffers):
                        buffers[idx].write(offset, val)
                except ValueError:
                    print("Invalid input")

            elif choice == '4':
                try:
                    idx = int(input("Index: "))
                    offset = int(input("Offset: "))
                    if 0 <= idx < len(buffers):
                        res = buffers[idx].read(offset)
                        print(f"Read: {res.hex()}")
                except ValueError:
                    print("Invalid input")

            elif choice == '5':
                try:
                    idx = int(input("Index: "))
                    if 0 <= idx < len(buffers):
                        print(f"Revealed: {hex(buffers[idx].addr())}")
                except ValueError:
                    print("Invalid input")

            elif choice == '6':
                try:
                    val = int(input("Value: "))
                    vault.append((val,))
                    print(f"Stored {len(vault)-1}")
                except ValueError:
                    print("Invalid input")

            elif choice == '7':
                try:
                    idx = int(input("Index: "))
                    if 0 <= idx < len(vault):
                        print(f"Restored: {vault[idx]}")
                except ValueError:
                    print("Invalid input")

            elif choice == '8':
                break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
