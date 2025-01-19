from datetime import datetime

CURRENT_YEAR = datetime.now().year


def get_battery_health():
    pass


def parse_date(lunch_information: list[dict]) -> tuple:
    made_at = int()
    status = int()
    for lunch_data in lunch_information:
        for key, value in lunch_data.items():
            if key == "Announced":
                try:
                    made_at = int(value.split(",")[0])
                except ValueError:
                    print(value)
                    pass
            elif key == "Status":
                status = 1 if "Available" in value else 0
    made_at = CURRENT_YEAR - made_at if made_at else 0
    return made_at, status


def parse_5g(network_options: list[dict]) -> bool:
    for option_json in network_options:
        for key, _ in option_json.items():
            if "5G" in key:
                return True
    return False
