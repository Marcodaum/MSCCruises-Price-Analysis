class Cruise:
    def __init__(self, cruise_id, ship_name, duration, price):
        self.cruise_id = cruise_id
        self.ship_name = ship_name
        self.duration = duration
        self.price = price
        self.price_per_night = int(int(price) / int(duration))

    # Attributes data-v-68983be6 and data-v-ec16924a
    cruise_id = None
    # Attribute class="ship-name"
    ship_name = None

    #departure_date = None
    # Attribute data-v-68983be6
    departure_port = None
    #arrival_date = None
    arrival_port = None
    # Attribute data-v-00ce0371
    duration = 0
    price = 0