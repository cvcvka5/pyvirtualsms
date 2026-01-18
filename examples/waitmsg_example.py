from pyvirtualsms import GSMDistributor, Provider

dist = GSMDistributor(provider=Provider.RECEIVESMSS)
phone = dist.get_random_number(country="germany")
print("Chosen phone:", phone)

print("Waiting for msg:")
print(dist.wait_for_message(phone, sender_contains="Easy", timeout=600, interval=25))
