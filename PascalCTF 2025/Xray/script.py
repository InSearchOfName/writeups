key = [0x2a, 0x37, 0x5e, 0x74, 0x56, 0x72, 0x34, 0x46,
       0x5a, 0x23, 0x37, 0x53, 0x34, 0x52, 0x46, 0x4e,
       0x64, 0x32]

encrypted = [0x78, 0x52, 0x08, 0x47, 0x24, 0x47, 0x07, 0x19,
             0x6b, 0x50, 0x68, 0x67, 0x43, 0x61, 0x35, 0x7e,
             0x09, 0x01]

flag = ''.join(chr(e ^ k) for e, k in zip(encrypted, key))

print(f"pascalCTF{{{flag}}}")