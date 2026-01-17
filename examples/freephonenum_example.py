from pyvirtualsms import GSMDistributor, Provider

# Example usage of the SMS24Me provider.
# This script demonstrates:
#   - Listing available countries
#   - Selecting a random number
#   - Fetching paginated messages
#   - Fetching numbers for a specific country

# Initialize the distributor with the SMS24Me provider.
dist = GSMDistributor(Provider.FREEPHONENUM)

# Fetch and display all available countries.
countries = dist.get_countries()
print("Available countries:", countries)

# Available numbers
print("Available numbers:", dist.get_numbers(country="canada"))

# Select a random phone number.
phone = dist.get_random_number()
print("Selected number:", phone)


# Fetch messages
msgs = dist.get_messages(phone)

print("Messages", msgs)

# Demonstrate case-insensitive country lookup for numbers.
us_numbers = dist.get_numbers(country="uniTEd states")
print("US number(s):", us_numbers)

