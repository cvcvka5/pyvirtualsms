from pyvirtualsms import GSMDistributor, Provider

# Example usage of the ReceiveSMSS provider.
# This script demonstrates:
#   - Listing available countries
#   - Fetching numbers for a given country (case-insensitive)
#   - Picking a random number
#   - Fetching messages, including a specific page (if supported by the provider)

# Initialize the distributor with the ReceiveSMSS provider.
dist = GSMDistributor(provider=Provider.RECEIVESMSS)

# Fetch and display all available countries.
countries = dist.get_countries()
print("Countries\n", countries)

# Fetch available numbers for a specific country.
# Country name matching is case-insensitive and provider-dependent.
numbers = dist.get_numbers(country="CroAtiA")
print("\n\nNumbers\n", numbers)

# Select a random phone number from the retrieved list.
phone = dist.get_random_number()
print("\n\nChosen\n", phone)

# Fetch messages for the chosen phone.
# For providers without pagination support, the distributor will ignore `page`.
messages_page_2 = dist.get_messages(phone, page=2)
print("\n\nMessages (page=2)\n", messages_page_2)

# Fetch all messages (or first page, depending on provider implementation)
# and show how many messages are currently available.
all_messages = dist.get_messages(phone)
print("\n\nNumber of messages: ", len(all_messages))
