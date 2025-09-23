groups = [
    {
        "name": "sales",
        "permissions": [
            {
                "code": "sales.view_sale",
                "description": "View sales details"
            },
            {
                "code": "sales.add_sale",
                "description": "Create new sales"
            },
            {
                "code": "sales.change_sale",
                "description": "Updating sale details (like the payments, quantities sold etc)"
            },
            {
                "code": "payments.add_payment",
                "description": "Enables to add payment details at Point Of Sale area."
            },
            {
                "code": "payments.change_payment",
                "description": "Updating payment details (like the date and price)"
            },
        ]
    },
    {
        "name": "stock_management",
        "permissions": [
            {
                "code": "products.view_branchproduct",
                "description": "View products of a branch"
            },
            {
                "code": "stock.view_stockbatch",
                "description": "View stock details"
            },
            {
                "code": "stock.add_stockbatch",
                "description": "Restock products"
            },
            {
                "code": "stock.change_stockbatch",
                "description": "Update stock details (like the quantities stocked and stock costs etc)"
            },
        ]
    },
    {
        "name": "user_management",
        "permissions": [
            {
                "code": "users.view_user",
                "description": "View users, their details and activity"
            },
            {
                "code": "users.change_user",
                "description": "Edit user details"
            },
            {
                "code": "users.add_user",
                "description": "Create a new user"
            },
        ]
    },
    {
        "name": "product_management",
        "permissions": [
            {
                "code": "products.view_product",
                "description": "View products"
            },
            {
                "code": "products.change_product",
                "description": "Edit product details"
            },
            {
                "code": "products.add_product",
                "description": "Create a new product"
            },
            {
                "code": "products.add_branchproduct",
                "description": "Assign products to branches"
            },
            {
                "code": "products.view_branchproduct",
                "description": "View a branch's products"
            },
        ]
    },
    {
        "name": "finance_management",
        "permissions": [
            {
                "code": "stock.view_stockbatch",
                "description": "View stock details"
            },
            {
                "code": "payments.view_payment",
                "description": "View payment details"
            },
            {
                "code": "sales.analyze_profit",
                "description": "Analyze sales profit and performance"
            },
        ]
    },
]