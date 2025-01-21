from datetime import datetime

CURRENT_YEAR = datetime.now().year
EUR_TO_USD = 1.03


def parse_price(misc_information: list[dict]):
    for misc_data in misc_information:
        for key, value in misc_data.items():
            if key == "Price":
                processed_prices = value.replace(" ", "").replace(" ", "")
                if "$" in value:
                    processed_prices = processed_prices.split("/")
                    for processed_price in processed_prices:
                        if "$" in processed_price:
                            price = ""
                            for char in processed_price:
                                if char.isdigit():
                                    price += char
                                elif char == ".":
                                    price += "."
                            return round(float(price), 1)
                elif "EUR" in value:
                    price = ""
                    for char in value:
                        if char.isdigit():
                            price += char
                        elif char == ".":
                            price += "."
                    return round(float(price) * EUR_TO_USD, 1)


def get_battery(battery_information: list[dict]) -> int:
    for battery_data in battery_information:
        for key, value in battery_data.items():
            if key == "Type":
                try:
                    result = int(''.join(char for char in value if char.isdigit()))
                except ValueError:
                    return 0
                return result if result < 11000 else 0

    return 0


def parse_display_information(display_information: list[dict]) -> tuple:
    resolution = int()
    size = float()
    for display_data in display_information:
        for key, value in display_data.items():
            if key == "Resolution" and not resolution:
                resolution_string = value.split(",")[0].replace(" ", "").split("x")
                resolution = int("".join(char for char in resolution_string[0] if char.isdigit())) * int(
                    "".join(char for char in resolution_string[1] if char.isdigit()))
            elif key == "Size" and not size:
                size = ""
                for char in value.split(",")[0]:
                    if char.isdigit():
                        size += char
                    elif char == ".":
                        size += "."
            try:
                size = float(size)
            except ValueError:
                print(key, value)
    return resolution, size


def parse_date(lunch_information: list[dict]) -> tuple:
    made_at = int()
    status = int()
    for lunch_data in lunch_information:
        for key, value in lunch_data.items():
            if key == "Announced":
                try:
                    made_at = int(value.split(",")[0])
                except ValueError:
                    made_at = 0
                    status = 2
                    return made_at, status
                    pass
            elif key == "Status":
                status = 1 if "Available" in value else 0
    made_at = CURRENT_YEAR - made_at if made_at else 0
    return made_at, status


def os_parser(platform_information: list[dict]) -> int:
    """
    param platform_information:
    return:
    1:Android
    2:IOS/IPadOS
    3:Others
    """

    # default os value: Android
    for platform_data in platform_information:
        for key, value in platform_data.items():
            if key == "OS":
                value = value.lower().split(" ")[0]
                if "android" in value:
                    return 1
                elif "ios" == value or "ipados" == value:
                    return 2
                else:
                    return 3
    return 1


def parse_5g(network_options: list[dict]) -> int:
    for option_json in network_options:
        for key, _ in option_json.items():
            if "5G" in key:
                return 1
    return 0


def parse_memory_data(memory_information: list[dict]) -> tuple:
    for memory_data in memory_information:
        for key, value in memory_data.items():
            if key == "Internal":
                if "GB" not in value:
                    continue
                if "MB" in value:
                    return 0, 0
                parsed_data = value.split(',')[0].split(" RAM")[0].replace("GB", "").split(" ")
                try:
                    parsed_data[1]
                except IndexError:
                    parsed_data.append(None)
                if parsed_data[0] and parsed_data[1]:
                    ram = float(parsed_data[1])
                    storage = float(parsed_data[0])
                    return ram, storage
                else:
                    if not parsed_data[1]:
                        ram = float(value.split(',')[1].split(" RAM")[0].replace("GB", "").split(" ")[1])
                    else:
                        ram = float(parsed_data[1])
                    if not parsed_data[0]:
                        storage = value.split(',')[1].split(" RAM")[0].replace("GB", "").split(" ")[0]
                    else:
                        storage = float(parsed_data[0])
                    return ram, storage
    return 0, 0
