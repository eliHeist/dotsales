permission_groups = [
    {
        "name": "Branches",
        "permissions": [
            {
                "code": "companies.add_branch",
                "description": "Creating Branches"
            },
            {
                "code": "companies.change_branch",
                "description": "Updating Branch Details"
            },
        ]
    },
    {
        "name": "Users",
        "permissions": [
            {
                "code": "users.view_user",
                "description": "View users details"
            },
            {
                "code": "users.add_user",
                "description": "Create new users"
            },
            {
                "code": "users.change_user",
                "description": "Updating user details"
            },
        ]
    },
    {
        "name": "Products",
        "permissions": [
            {
                "code": "products.view_product",
                "description": "View products details"
            },
            {
                "code": "products.add_product",
                "description": "Create new products"
            },
            {
                "code": "products.change_product",
                "description": "Updating product details (like name)"
            },
        ]
    },
    {
        "name": "Sales",
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
        ]
    },
    {
        "name": "Stock Management",
        "permissions": [
            {
                "code": "stocks.view_stock",
                "description": "View stock details"
            },
            {
                "code": "stocks.add_stock",
                "description": "Restock products"
            },
            {
                "code": "stocks.change_stock",
                "description": "Updating stock details (like the selling prices, quantities stocked etc)"
            },
            {
                "code": "stocks.delete_stock",
                "description": "Deleting stock records"
            },
        ]
    },
]