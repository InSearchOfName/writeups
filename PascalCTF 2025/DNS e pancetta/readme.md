# Description
I've recently started studying a new cooking book and I think I've found the best recipe ever.
Do you wanna read it? Ask my dear friend DNS!

## Info

- Solved by [InSearchOfName](https://github.com/InSearchOfName)
- Written by [InSearchOfName](https://github.com/InSearchOfName)

## Solution

When opening the pcapng file we see the attacker is sending queries for random subdomains but all these subdomains are hexencdoded 

so what we do is we extract all the subdomains with this command

~~~bash
tshark -r pancetta.pcapng -Y "dns.qry.name && ip.src == 172.19.0.3" -T fields -e dns.qry.name | cut -d '.' -f1 > extracted_hex.txt
~~~

after that we can decode the hex txt using this

~~~bash
cat extracted_hex.txt | xxd -r -p
~~~

Then we see our flag `pascalCTF{DNS_b34coning_4ll_over_the_place}`

