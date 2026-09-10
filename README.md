# AI E-Commerce Customer Support Agent

A dependency-free Python terminal prototype based on the project report. It demonstrates core agentic AI patterns in an e-commerce support scenario: intent routing, tool calling, customer memory, and structured demo data.

## Features

- Product search with names, prices, categories, and descriptions
- Order tracking with status and expected delivery
- Return request creation with request IDs
- Product recommendations
- Session memory for the customer's name
- Simple natural-language intent routing
- Visible tool selection for learning and demonstrations

## Run locally

Requires Python 3.9 or newer. No external packages are required.

    python app.py

Try these messages in the terminal:

    find wireless headphones
    track ORD-1001
    return ORD-1002
    recommend something for travel
    my name is Ray
    what is my name

## Project structure

- `app.py` - agent logic, tools, sample catalog, sample orders, and terminal chat loop
- `README.md` - setup, features, and usage
- `.gitignore` - Python development exclusions

## How the agent works

1. The customer enters a message.
2. The router identifies a likely intent using lightweight rules.
3. The agent selects one registered tool.
4. The tool searches data or changes in-memory demo state.
5. The result is returned to the customer.

## Important limitation

This is an educational prototype. Product and order data are hard-coded demo records, return requests exist only during the current process, and no real payment, delivery, database, authentication, or large language model service is connected.

## Future enhancements

- Replace sample data with SQLite, PostgreSQL, or MongoDB
- Add a Flask or FastAPI web interface
- Connect a large language model for flexible intent detection
- Add customer authentication and order history
- Integrate real-time shipping, returns, refund, and payment APIs
- Add tests, logging, rate limits, and role-based access control