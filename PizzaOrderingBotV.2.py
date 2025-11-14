class PizzaOrder:
    size: str = ""
    crust: str = ""
    toppings: List[str] = None
    delivery: bool = False
    address: str = ""
    total: float = 0.0
    created_at: str = ""

    def __post_init__(self):
        if self.toppings is None:
            self.toppings = []
        if not self.created_at:
            self.created_at = datetime.datetime.now().isoformat(timespec='seconds')
# Pricing
SIZE_PRICE = {"small": 8.0, "medium": 10.0, "large": 12.0}
CRUST_PRICE = {"thin": 0.0, "regular": 1.0, "stuffed": 3.0}
TOPPING_PRICE = 0.75
DELIVERY_FEE = 3.0

def ask_choice(prompt: str, options: List[str]) -> str:
    opts = "/".join(options)
    options_set = {o.lower() for o in options}
    while True:
        ans = input(f"{prompt} ({opts}): ").strip().lower()
        if ans in options_set:
            return ans
        print("Invalid choice — try again.")

def yes_no(prompt: str) -> bool:
    return ask_choice(prompt, ["yes", "no"]) == "yes"

def get_toppings() -> List[str]:
    print("Enter toppings one per line (blank to finish). Common toppings: pepperoni, mushrooms, onions, olives, sausage, bacon, peppers")
    toppings = []
    while True:
        t = input("> ").strip()
        if t == "":
            break
        toppings.append(t)
    return toppings

def calculate_total(order: PizzaOrder) -> float:
    total = SIZE_PRICE[order.size] + CRUST_PRICE[order.crust]
    total += len(order.toppings) * TOPPING_PRICE
    if order.delivery:
        total += DELIVERY_FEE
    return round(total, 2)

def save_order_csv(order: PizzaOrder, filename: str = "orders.csv") -> None:
    fieldnames = ["created_at", "size", "crust", "toppings", "delivery", "address", "total"]
    row = {
        "created_at": order.created_at,
        "size": order.size,
        "crust": order.crust,
        "toppings": ";".join(order.toppings),
        "delivery": "yes" if order.delivery else "no",
        "address": order.address,
        "total": f"{order.total:.2f}"
    }
    try:
        write_header = False
        try:
            with open(filename, "r", newline="", encoding="utf-8") as f:
                pass
        except FileNotFoundError:
            write_header = True
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(row)
    except Exception as e:
        print(f"Warning: could not save order to CSV ({e})")

def print_summary(order: PizzaOrder) -> None:
    print("\n--- Order Summary ---")
    print(f"Size: {order.size.capitalize()}   Crust: {order.crust.capitalize()}")
    print(f"Toppings: {', '.join(order.toppings) if order.toppings else 'none'}")
    print(f"Delivery: {'Yes' if order.delivery else 'No'}")
    if order.delivery:
        print(f"Address: {order.address}")
    print(f"Total: ${order.total:.2f}")

def main():
    print("Welcome to EduPizza (Python)!")
    while True:
        order = PizzaOrder()
        order.size = ask_choice("Choose size", list(SIZE_PRICE.keys()))
        order.crust = ask_choice("Choose crust", list(CRUST_PRICE.keys()))
        order.toppings = get_toppings()
        order.delivery = yes_no("Delivery?")
        if order.delivery:
            order.address = input("Enter delivery address: ").strip()
        order.total = calculate_total(order)
        print_summary(order)

        if yes_no("Confirm order?"):
            print("Thanks — your order is placed!")
            # Save order (optional)
            if yes_no("Save this order to orders.csv?"):
                save_order_csv(order)
                print("Order saved to orders.csv")
        else:
            print("Order cancelled.")

        if not yes_no("Would you like to place another order?"):
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()