from pyvirtualsms.distributor import GSMDistributor
from pyvirtualsms.models import Provider

if __name__ == "__main__":
    dist = GSMDistributor(Provider.SMS24ME)

    countries = dist.get_countries()
    print("Available countries:", countries)

    phone = dist.get_random_number()
    print("Selected number:", phone)

    msgs_page_1 = dist.get_messages(phone, page=1)
    msgs_page_2 = dist.get_messages(phone, page=2)

    print("Messages page 1:", msgs_page_1)
    print("Messages page 2:", msgs_page_2)

