from django.urls import path, include

app_configs = [
	{ 'app_name': 'app.branches', 'url': 'branches/', 'namespace': 'branches' },

	{ 'app_name': 'app.company', 'url': '', 'namespace': 'company' },

	{ 'app_name': 'api', 'url': 'api_views/', 'namespace': 'api_views' },

	{ 'app_name': 'finances.payments', 'url': 'finances/payments/', 'namespace': 'payments' },

	{ 'app_name': 'accounts.companies', 'url': 'accounts/companies/', 'namespace': 'companies' },

	{ 'app_name': 'inventory.sales', 'url': 'inventory/sales/', 'namespace': 'sales' },

	{ 'app_name': 'accounts.users', 'url': 'accounts/', 'namespace': 'users' },

	{ 'app_name': 'inventory.stock', 'url': 'inventory/stock/', 'namespace': 'stock' },

	{ 'app_name': 'inventory.products', 'url': 'inventory/products/', 'namespace': 'products' },

    # { "app_name": "finances.payments", "url": "finances/payments", "namespace": "payments" },
]

def getAppUrls():
    urlpatterns = []
    for config in app_configs:
        urlpatterns.append(
            path(f"{config['url']}", include(f"{config['app_name']}.urls", namespace=config['namespace']))
        )
    return urlpatterns

def getAppNames():
    return [config['app_name'] for config in app_configs]
