import sqlite3

# Helper function to search the database for a card given its name. 
# Returns the entire row of the card if found, otherwise returns None.
def seach_database(card_name):
    connection = sqlite3.connect("carddatabase.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cards WHERE name = (?)", (card_name,))
    rows = cursor.fetchone()
    if rows is None:
        connection.close()
        return None

    data = list(rows)
    connection.close()

    return data


# Returns following information of a card given its name. 
#   - name
#   - mana_cost
#   - cmc
#   - type_line
#   - keywords
#   - oracle_text
#   - power
#   - toughness
#   - colors
#   - color_identity
# print_data is a boolean that determines whether to print the information or not.
def get_card_info(card_name, print_data=False):

    card_data = seach_database(card_name)

    if print_data:
        print(card_data[3:])

    return card_data[3:]


# Returns the type line of a card given its name. print_data is a boolean that 
# determines whether to print the type line or not.
def get_type_line(card_name, print_data=False):

    card_data = seach_database(card_name)
    
    if print_data:
        print(card_data[-7])

    return card_data[-7]


# Returns the color of a card given its name. print_data is a boolean that 
# determines whether to print the color or not.
def get_color(card_name, print_data=False):

    card_data = seach_database(card_name)
    
    if print_data:
        print(card_data[-2])

    return card_data[-2]


# Returns the color identity of a card given its name. print_data is a boolean that 
# determines whether to print the color identity or not.
def get_color_identity(card_name, print_data=False):

    card_data = seach_database(card_name)

    # Set the color identity to "C" if the card is colorless (i.e. has no color identity)
    identity = card_data[-1] if card_data[-1] else "C"
    
    if print_data:
        print(identity)

    return identity


# Returns a list of playable cards given a card name. A card is considered playable 
# if its color identity is a subset of the color identity of the given card or the 
# card is colorless.
def get_playable_cards(card_name):

    # Add colorless to the identity of the card to allow for colorless cards to be playable
    identity = get_color_identity(card_name) + ", C"

    connection = sqlite3.connect("carddatabase.db")
    cursor = connection.cursor()

    # Get all cards from the database
    cursor.execute("SELECT * FROM cards")

    rows = cursor.fetchall()

    playable_cards = []


    for row in rows:
        card_identity = row[-1] if row[-1] else "C"

        # Convert "W,U,B" into ["W", "U", "B"]
        card_colors = set(card_identity.split(",")) if card_identity else set()

        # Check if every color on the card is allowed
        if card_colors.issubset(set(identity)):
            playable_cards.append(list(row))

    connection.close()

    return playable_cards



if __name__ == "__main__": 

    get_card_info("The Ur-Dragon", print_data=True)
    get_type_line("Hearthhull, the Worldseed", print_data=True)
    get_color("Sliver Overlord", print_data=True)
    get_color_identity("Meren of Clan Nel Toth", print_data=True)

    for card in get_playable_cards("Molecule Man")[:3]:
        print(card[3])