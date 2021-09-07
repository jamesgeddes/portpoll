# portpoll
Takes in a list of IP addresses and a list of ports then uses multithreading to scan all nodes simultaneously. Outputs 

`datetime`, `IP`, `port`, `alive`

Either pass in a text file of IP addresses, and a separate text file of ports, one per line, or pass in a list of each directly.

Can be handy if you need to run in an environment where you only have python available, for example. No fancy GUI, just CLI.