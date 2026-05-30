
#!/usr/bin/python3
import base64
import sys
import codecs

# total arguments
n = len(sys.argv)
file =""
if n != 2:
	print("invalid argument amount: file only")
	exit()
else:
	file = sys.argv[1]

file = codecs.open(file, 'rb')
content = file.read()
hostname=".domainforhire.aws.jerseyctf.com"

base64_encoded = base64.b64encode(content)
total_read = 0
start = 0
end = 4

while total_read <= len(base64_encoded):
	payload  = base64_encoded[start:end]
	total_read += 4
	start += 4
	end += 4
	if payload == b'':
		exit()
	FQDN = payload.decode("utf-8") + hostname
	print(FQDN)