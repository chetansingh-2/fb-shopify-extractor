import shopify
from datetime import datetime, timedelta
from ..config import SHOPIFY_SHOP_URL, SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SHOPIFY_API_VERSION
from ..models.shopify_model import ShopifyProduct, ShopifyOrder, ShopifyProductVariant



class ShopifyService:
    def __init__(self):
        self.session = shopify.Session(SHOPIFY_SHOP_URL, SHOPIFY_API_VERSION, SHOPIFY_API_SECRET)
        shopify.ShopifyResource.activate_session(self.session)
        
    def __del__(self):
        shopify.ShopifyResource.clear_session()
        
    def authenticate(self):
        shopify.Session.setup(api_key=SHOPIFY_API_KEY, secret=SHOPIFY_API_SECRET)
        
    def get_products(self, limit=50):
        products_data = []
        products = shopify.Product.find(limit=limit)
        
        for product in products:
            product_dict = product.to_dict()
            variants = []
            
            for variant in product_dict['variants']:
                variants.append(ShopifyProductVariant(
                    id=variant['id'],
                    product_id=variant['product_id'],
                    title=variant['title'],
                    price=variant['price'],
                    sku=variant.get('sku'),
                    inventory_quantity=variant.get('inventory_quantity', 0)
                ))
                
            products_data.append(ShopifyProduct(
                id=product_dict['id'],
                title=product_dict['title'],
                product_type=product_dict.get('product_type'),
                created_at=product_dict['created_at'],
                updated_at=product_dict['updated_at'],
                variants=variants
            ))
            
        return products_data
    
    def get_orders(self, days=30, limit=50):
        orders_data = []
        date_threshold = datetime.now() - timedelta(days=days)
        date_str = date_threshold.isoformat()
        
        orders = shopify.Order.find(created_at_min=date_str, limit=limit)
        
        for order in orders:
            order_dict = order.to_dict()
            orders_data.append(ShopifyOrder(
                id=order_dict['id'],
                order_number=order_dict['order_number'],
                customer=order_dict.get('customer'),
                created_at=order_dict['created_at'],
                total_price=order_dict['total_price'],
                line_items=order_dict['line_items']
            ))
            
        return orders_data