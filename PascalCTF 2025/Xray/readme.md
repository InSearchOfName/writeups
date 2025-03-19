# Description
I've recently written my first license checker, maybe Steam will buy it...

Flag format: `pascalCTF{secret_signature}`

## Info

- Solved by [Chomken](https://github.com/chomken)
- Written by [InSearchOfName](https://github.com/InSearchOfName)

## Solution

First we want to know what kind of file it is this we do by running

~~~bash
file x-ray
~~~

once we run that command we get this back `x-ray: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 4.4.0, BuildID[sha1]=8b10118f03bac275f6871504ea04c5b078a0f038, not stripped
`

after that we know what kind of file it is so now we open the file in ghidra.

firstly we will go check the main function in the Functions tree. there we see the following code
~~~c++
undefined8 main(void)

{
  char cVar1;
  int iVar2;
  size_t sVar3;
  long in_FS_OFFSET;
  char local_48 [56];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  fwrite("Insert the secret code: ",1,0x18,stdout);
  fgets(local_48,0x32,stdin);
  sVar3 = strlen(local_48);
  iVar2 = (int)sVar3;
  if ((0 < iVar2) && (local_48[iVar2 + -1] == '\n')) {
    local_48[iVar2 + -1] = '\0';
  }
  cVar1 = checkSignature(local_48);
  if (cVar1 == '\0') {
    fwrite("Sorry, the secret code is wrong!",1,0x20,stdout);
  }
  else {
    printf("Congrats! You have found the secret code, pascalCTF{%s}",local_48);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
~~~

We see that cVar calls the method `checkSignature` which contains the following code

~~~c++
undefined8 checkSignature(char *param_1)

{
  size_t sVar1;
  undefined8 uVar2;
  uint local_c;
  
  sVar1 = strlen(param_1);
  if (sVar1 == 0x12) {
    for (local_c = 0; local_c < 0x12; local_c = local_c + 1) {
      if ((char)(param_1[(int)local_c] ^ key[(int)local_c]) != encrypted[(int)local_c]) {
        return 0;
      }
    }
    uVar2 = 1;
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}
~~~

so we see that for each char in our param that there is a XOR operation between our char and the key and then they are compared to check if they are not equal.
so now we know that `key` and `encrypted` are important

now we do an objectdump and we grep encrypted and key with the following command
~~~bash
 
┌──(kali㉿kali)-[~/Desktop]
└─$ objdump -D x-ray | grep key
    11bc:       48 8d 15 4d 0e 00 00    lea    0xe4d(%rip),%rdx        # 2010 <key>
0000000000002010 <key>:
                                                                                                                                                                                   
┌──(kali㉿kali)-[~/Desktop]
└─$ objdump -D x-ray | grep encrypted
    11ce:       48 8d 15 5b 0e 00 00    lea    0xe5b(%rip),%rdx        # 2030 <encrypted>
    122c:       48 8d 05 10 0e 00 00    lea    0xe10(%rip),%rax        # 2043 <encrypted+0x13>
    129e:       48 8d 05 bb 0d 00 00    lea    0xdbb(%rip),%rax        # 2060 <encrypted+0x30>
    12c8:       48 8d 05 c9 0d 00 00    lea    0xdc9(%rip),%rax        # 2098 <encrypted+0x68>
    2013:       74 56                   je     206b <encrypted+0x3b>
    2015:       72 34                   jb     204b <encrypted+0x1b>
0000000000002030 <encrypted>:
    2030:       78 52                   js     2084 <encrypted+0x54>
    203f:       7e 09                   jle    204a <encrypted+0x1a>
    2045:       73 65                   jae    20ac <encrypted+0x7c>
    2053:       74 20                   je     2075 <encrypted+0x45>
    206c:       75 20                   jne    208e <encrypted+0x5e>
    2082:       74 20                   je     20a4 <encrypted+0x74>
    2092:       46 7b 25                rex.RX jnp 20ba <encrypted+0x8a>
~~~

then we debug the file with gdb
~~~bash
└─$ gdb x-ray 
(gdb) break checkSignature
Breakpoint 1 at 0x117d
(gdb) run
Starting program: /home/kali/Desktop/x-ray 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Insert the secret code: sigma

Breakpoint 1, 0x000055555555517d in checkSignature ()
~~~
First we we place a breakpoint on the function `checkSignature` after that we run the program so we can reach said breakpoint

Now that we have reached the breakpoint we are going to look at all the memory adresses
~~~bash
(gdb) info proc mappings
process 134498
Mapped address spaces:

Start Addr         End Addr           Size               Offset             Perms File 
0x0000555555554000 0x0000555555555000 0x1000             0x0                r--p  /home/kali/Desktop/x-ray 
0x0000555555555000 0x0000555555556000 0x1000             0x1000             r-xp  /home/kali/Desktop/x-ray 
0x0000555555556000 0x0000555555557000 0x1000             0x2000             r--p  /home/
...
~~~

we do a little bit of math and we do the first memory address + the adress of `encrypted` and `key`

which comes out to `0x555555556010` for the `key` and to `0x555555556030` for `encrypted`
~~~bash
(gdb) x/18xb 0x555555556010
0x555555556010 <key>:   0x2a    0x37    0x5e    0x74    0x56    0x72    0x34    0x46
0x555555556018 <key+8>: 0x5a    0x23    0x37    0x53    0x34    0x52    0x46    0x4e
0x555555556020 <key+16>:        0x64    0x32
(gdb) x/18xb 0x555555556030
0x555555556030 <encrypted>:     0x78    0x52    0x08    0x47    0x24    0x47    0x07    0x19
0x555555556038 <encrypted+8>:   0x6b    0x50    0x68    0x67    0x43    0x61    0x35    0x7e
0x555555556040 <encrypted+16>:  0x09    0x01
(gdb) exit
~~~
now we that we got the values out of the keys we must decrypt them which we will do with the following python script
~~~py
key = [0x2a, 0x37, 0x5e, 0x74, 0x56, 0x72, 0x34, 0x46,
       0x5a, 0x23, 0x37, 0x53, 0x34, 0x52, 0x46, 0x4e,
       0x64, 0x32]

encrypted = [0x78, 0x52, 0x08, 0x47, 0x24, 0x47, 0x07, 0x19,
             0x6b, 0x50, 0x68, 0x67, 0x43, 0x61, 0x35, 0x7e,
             0x09, 0x01]

flag = ''.join(chr(e ^ k) for e, k in zip(encrypted, key))

print(f"pascalCTF{{{flag}}}")
~~~

and then we get the following output of the script `pascalCTF{ReV3r53_1s_4w3s0m3}` which is also our flag.