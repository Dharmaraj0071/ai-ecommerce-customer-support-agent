"""AI E-Commerce Customer Support Agent demo.

A dependency-free terminal prototype demonstrating agent routing,
tool calling, and lightweight customer memory.
"""

from __future__ import annotations

import re
from typing import Callable


PRODUCTS = [
    {
        "id": "P001",
        "name": "Classic Cotton Shirt",
        "category": "clothing",
        "price": 29.99,
        "description": "Breathable cotton shirt in multiple colors.",
    },
    {
        "id": "P002",
        "name": "Slim Fit Jeans",
        "category": "clothing",
        "price": 49.99,
        "description": "Stretch denim jeans with a modern slim fit.",
    },
    {
        "id": "P003",
        "name": "Wireless Headphones",
        "category": "electronics",
        "price": 79.99,
        "description": "Bluetooth headphones with noise reduction.",
    },
    {
        "id": "P004",
        "name": "Smart Watch",
        "category": "electronics",
        "price": 119.99,
        "description": "Fitness tracking, notifications, and a long-lasting battery.",
    },
    {
        "id": "P005",
        "name": "Everyday Backpack",
        "category": "accessories",
        "price": 39.99,
        "description": "Water-resistant backpack for work and travel.",
    },
]

ORDERS = {
    "ORD-1001": {
        "product": "Wireless Headphones",
        "status": "Shipped",
        "expected_delivery": "2026-09-14",
    },
    "ORD-1002": {
        "product": "Classic Cotton Shirt",
        "status": "Processing",
        "expected_delivery": "2026-09-17",
    },
    "ORD-1003": {
        "product": "Smart Watch",
        "status": "Delivered",
        "expected_delivery": "2026-09-08",
    },
}

CUSTOMER_MEMORY: dict[str, str] = {}
RETURN_REQUESTS: list[dict[str, str]] = []


def format_product(product: dict) -> str:
    return (
        f"{product['name']} ({product['id']}) - ${product['price']:.2f}\n"
        f"  Category: {product['category']} | {product['description']}"
    )


def search_products(keyword: str) -> str:
    """Find products whose name, category, or description matches the query."""
    words = [
        word
        for word in re.findall(r"[a-z0-9]+", keyword.lower())
        if word not in {"show", "me", "please"}
    ]
    matches = [
        product
        for product in PRODUCTS
        if any(
            word
            in f"{product['name']} {product['category']} {product['description']}".lower()
            for word in words
        )
    ]
    if not matches:
        return (
            "I could not find a matching product. Try shirts, jeans, "
            "headphones, watches, or backpacks."
        )
    return "Matching products:\n\n" + "\n\n".join(
        format_product(product) for product in matches
    )


def track_order(order_id: str) -> str:
    """Return the current status of a demo order."""
    order = ORDERS.get(order_id.upper())
    if not order:
        return f"I could not find order {order_id}. Check the order number and try again."
    return (
        f"Order {order_id.upper()}\n"
        f"Product: {order['product']}\n"
        f"Status: {order['status']}\n"
        f"Expected delivery: {order['expected_delivery']}"
    )


def create_return(order_id: str, reason: str) -> str:
    """Create a return request for a known demo order."""
    order_id = order_id.upper()
    if order_id not in ORDERS:
        return f"I cannot create a return for {order_id} because the order was not found."
    if any(item["order_id"] == order_id for item in RETURN_REQUESTS):
        return f"A return request already exists for {order_id}."
    request_id = f"RET-{len(RETURN_REQUESTS) + 1:04d}"
    RETURN_REQUESTS.append(
        {"request_id": request_id, "order_id": order_id, "reason": reason}
    )
    return f"Return request {request_id} created for {order_id}. Reason: {reason}."


def recommend_products(preference: str = "") -> str:
    """Recommend up to three products using a simple preference match."""
    preference = preference.lower()
    matches = [
        product
        for product in PRODUCTS
        if preference
        and preference
        in f"{product['name']} {product['category']} {product['description']}".lower()
    ]
    selected = (matches or PRODUCTS)[:3]
    return "Based on your request, I recommend:\n\n" + "\n\n".join(
        format_product(product) for product in selected
    )


def remember_customer_name(name: str) -> str:
    CUSTOMER_MEMORY["name"] = name.strip().title()
    return f"Thanks, {CUSTOMER_MEMORY['name']}! I will remember your name during this session."


def get_customer_name() -> str:
    name = CUSTOMER_MEMORY.get("name")
    return f"Your name is {name}." if name else (
        "I do not know your name yet. Say: my name is ..."
    )


TOOLS: dict[str, Callable] = {
    "search_products": search_products,
    "track_order": track_order,
    "create_return": create_return,
    "recommend_products": recommend_products,
    "remember_customer_name": remember_customer_name,
    "get_customer_name": get_customer_name,
}


def run_tool(tool_name: str, **arguments) -> str:
    """Execute one of the agent's registered tools."""
    tool = TOOLS.get(tool_name)
    if not tool:
        return "The requested support tool is not available."
    return tool(**arguments)


def extract_order_id(text: str) -> str | None:
    match = re.search(r"\bORD-\d{4}\b", text.upper())
    return match.group(0) if match else None


def agent_reply(query: str) -> tuple[str, str]:
    """Classify a query, select a tool, and return its response."""
    normalized = query.strip()
    lower = normalized.lower()

    name_match = re.search(
        r"(?:my name is|i am|i'm)\s+([a-z][a-z .'-]+)",
        normalized,
        re.IGNORECASE,
    )
    if name_match:
        tool = "remember_customer_name"
        return tool, run_tool(tool, name=name_match.group(1))

    if "what is my name" in lower or "remember my name" in lower:
        tool = "get_customer_name"
        return tool, run_tool(tool)

    order_id = extract_order_id(normalized)
    if any(word in lower for word in ("return", "refund")):
        tool = "create_return"
        if not order_id:
            return tool, (
                "Please include an order number such as ORD-1001 "
                "to create a return request."
            )
        return tool, run_tool(
            tool,
            order_id=order_id,
            reason="Customer requested a return or refund",
        )

    if order_id and any(
        word in lower for word in ("order", "track", "status", "delivery", "delivered")
    ):
        tool = "track_order"
        return tool, run_tool(tool, order_id=order_id)

    if any(word in lower for word in ("recommend", "suggest", "what should i buy")):
        tool = "recommend_products"
        return tool, run_tool(tool, preference=normalized)

    if any(word in lower for word in ("search", "find", "looking for", "product", "buy")):
        tool = "search_products"
        return tool, run_tool(tool, keyword=normalized)

    if lower in {"help", "hello", "hi", "hey"}:
        return "help", (
            "I can help with product search, order tracking, returns, "
            "recommendations, and your name.\n"
            "Examples: find headphones | track ORD-1001 | "
            "return ORD-1002 | recommend something for travel"
        )

    return "help", (
        "I can help with products, orders, returns, recommendations, "
        "or customer memory. Type help for examples."
    )


def main() -> None:
    print("AI E-Commerce Customer Support Agent")
    print("Type help for examples, or quit to exit.")
    while True:
        try:
            query = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if query.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        if not query:
            continue
        tool_name, response = agent_reply(query)
        print(f"\n[tool selected: {tool_name}]\n{response}")


if __name__ == "__main__":
    main()