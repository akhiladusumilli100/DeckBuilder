import card_explorer



# Gets the card information for a given card name and prints it in neat format by default or verbose if neat = False.
# In neat format, it prints the name, mana cost, type line, oracle text, power/toughness, and color identity.
# In verbose format, it prints all the information available for the card.
def print_card_info(card_name, neat=True):
    card_info = card_explorer.get_card_info(card_name)

    if card_info is None:
        print("Error: Invalid Card Name")
        return

    if neat ==  False:
        print(f"Name: { card_info[0] }")
        print(f"Mana Cost: { card_info[1] }")
        print(f"CMC: { card_info[2] }")
        print(f"Type Line: { card_info[3] }")
        print(f"Keywords: { card_info[4] }")
        print(f"Oracle Text: { card_info[5] }")
        print(f"Power: { card_info[6] }")
        print(f"Toughness: { card_info[7] }")
        print(f"Colors: { card_info[8] }")
        print(f"Color Identity: { card_info[9] }")
    else:
        print(f"{ card_info[0] }")
        print(f"{ card_info[1] }")
        print(f"Type Line: { card_info[3] }")
        print(f"Oracle Text: { card_info[5] }")
        print(f"{ card_info[6] }/{ card_info[7] }")
        print(f"Color Identity: { card_info[9] }")


if __name__ == "__main__": 
    print("Welcome to the Card Explorer!")

    card_name = input("Please enter the name of the card you want to explore:")

    print("Fetching card information...\n")

    print_card_info(card_name)

