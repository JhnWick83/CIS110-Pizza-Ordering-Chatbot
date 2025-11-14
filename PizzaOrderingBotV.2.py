SECRET_NAME = "greg webb" 

CRUST_PRICES = {"thin": 0.0, "regular": 1.0, "stuffed": 3.0}
TOPPING_COST = 0.75


class PizzaOrder:
    
    def __init__(self):
        self.size = ""
        self.crust = ""
        self.toppings = []
        self.delivery = False
        self.address = ""
        self.total = 0.0
        self.created_at = datetime.datetime.now().isoformat(timespec='seconds')


def ask_user_choice(prompt, options): 
    opts = "/".join(options)
    valid_options = {o.lower() for o in options}
    while True:
        ans = input(f"{prompt} ({opts}): ").strip().lower()
        if ans in valid_options:
            return ans
        print("Invalid choice — try again.")

def is_yes(prompt): 
    return ask_user_choice(prompt, ["yes", "no"]) == "yes"

def collect_toppings(): 
    print("Enter toppings one per line (blank to finish). Common toppings: pepperoni, mushrooms, onions, olives, sausage, bacon, peppers")
    toppings_list = [] 
    while True:
        t = input("> ").strip()
        if not t:
            break
        toppings_list.append(t)
    return toppings_list

def calc_pizza_cost(size, crust, topping_count): 
    if size == "small":
        base_price = 8.99
    elif size == "medium":
        base_price = 14.99
    elif size == "large":
        base_price = 17.99
    else:
        base_price = 0.0 
        
    crust_price = CRUST_PRICES[crust]
    topping_price = topping_count * TOPPING_COST
    return round(base_price + crust_price + topping_price, 2)

def save_order(order, file_name="orders.csv"): 
    fields = ["created_at", "size", "crust", "toppings", "delivery", "address", "total"]
    data = {
        "created_at": order.created_at,
        "size": order.size,
        "crust": order.crust,
        "toppings": ";".join(order.toppings),
        "delivery": "yes" if order.delivery else "no",
        "address": order.address,
        "total": f"{order.total:.2f}"
    }
    
    write_header = False
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        write_header = True
            
    try:
        with open(file_name, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            if write_header:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        print(f"Warning: could not save order to CSV ({e})")

def show_summary(order): 
    print("\n--- Order Summary ---")
    print(f"Size: {order.size.capitalize()}   Crust: {order.crust.capitalize()}")
    print(f"Toppings: {', '.join(order.toppings) if order.toppings else 'none'}")
    print(f"Delivery: {'Yes' if order.delivery else 'No'}")
    if order.delivery:
        print(f"Address: {order.address}")
        
    if order.total >= 50.0:
        print("Congrats! You earned a $1 off coupon for your next order.") 
    else:
        pass 

    print(f"Total: ${order.total:.2f}")


def main():
    print("Welcome to EduPizza (Python)!")
    
    user_name = input("What's your name? (first and last): ").strip()
    
    if user_name.lower() == SECRET_NAME:
        print(f"Hey {user_name}, welcome back! You've unlocked the special greeting!")
    else:
        print(f"Hello {user_name}, thanks for stopping by!")

    while True:
        order = PizzaOrder() 

        order.size = ask_user_choice("Choose size", ["small", "medium", "large"])
        order.crust = ask_user_choice("Choose crust", list(CRUST_PRICES.keys()))
        order.toppings = collect_toppings()

        order.delivery = is_yes("Delivery?")
        
        if order.delivery:
            deliveryFee = 5.0
            order.address = input("Enter delivery address: ").strip()
        else:
            deliveryFee = 0.0

        pizza_cost = calc_pizza_cost(order.size, order.crust, len(order.toppings))
        order.total = round(pizza_cost + deliveryFee, 2)

        show_summary(order)

        if is_yes("Confirm order?"):
            print("Thanks — your order is placed!")
            if is_yes("Save this order to orders.csv?"):
                save_order(order)
                print("Order saved to orders.csv")
        else:
            print("Order cancelled.")

        if not is_yes("Would you like to place another order?"):
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
