# Description
I encrypted the flag but I don't remember in what order. Can you help me?

## Info

- Solved by [InSearchOfName](https://github.com/InSearchOfName)
- Written by [InSearchOfName](https://github.com/InSearchOfName)

# Solution
First we check the encryption script and we see it has been encrytped 10 times with 2 diffrent algoritms hex and base64

so we go to the cyberchef to make this easy and revert 10 times depending what algorithm we see so if we see base64 we decode base64 else we do hex decoding

once we have done that the recipe in cyberchef looks as the following
~~~
From_Hex('Auto')
From_Hex('Auto')
From_Hex('Auto')
From_Base64('A-Za-z0-9+/=',true,false)
From_Hex('Auto')
From_Base64('A-Za-z0-9+/=',true,false)
From_Hex('Auto')
From_Hex('Auto')
From_Hex('Auto')
From_Hex('Auto')
~~~

after doing that we get the following flag `pascalCTF{nex7_T1m3_ch3ck_cyb3rCH3F_$b64-d/e$}`