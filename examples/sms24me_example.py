from pyvirtualsms import GSMDistributor, Provider

# Example usage of the SMS24Me provider.
# This script demonstrates:
#   - Listing available countries
#   - Selecting a random number
#   - Fetching paginated messages
#   - Fetching numbers for a specific country

# Initialize the distributor with the SMS24Me provider.
dist = GSMDistributor(Provider.SMS24ME)

# Fetch and display all available countries.
countries = dist.get_countries()
print("Available countries:", countries)

# Fetch all numbers
print("Numbers:", dist.get_numbers())

# Select a random phone number.
phone = dist.get_random_number()
print("Selected number:", phone)

# Fetch messages from different pages (if the provider supports pagination).
msgs_page_1 = dist.get_messages(phone, page=1)
msgs_page_2 = dist.get_messages(phone, page=2)

print("Messages page 1:", msgs_page_1)
print("Messages page 2:", msgs_page_2)

# Demonstrate case-insensitive country lookup for numbers.
austria_numbers = dist.get_numbers(country="auStria")
print("Austria number(s):", austria_numbers)

