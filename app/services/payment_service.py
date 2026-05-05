import mercadopago
from flask import current_app
from app.models.order import Order
from app import db

class PaymentService:
    @staticmethod
    def get_sdk():
        return mercadopago.SDK(current_app.config['MP_ACCESS_TOKEN'])

    @staticmethod
    def create_pix_payment(order):
        sdk = PaymentService.get_sdk()
        
        payment_data = {
            "transaction_amount": float(order.total_amount),
            "description": f"Pedido #{order.id} - Fulô",
            "payment_method_id": "pix",
            "payer": {
                "email": order.user.email,
                "first_name": order.user.name.split()[0],
                "last_name": order.user.name.split()[-1] if len(order.user.name.split()) > 1 else "",
            },
            "notification_url": current_app.config['WEBHOOK_URL'],
            "external_reference": str(order.id)
        }
        
        payment_response = sdk.payment().create(payment_data)
        return payment_response["response"]

    @staticmethod
    def create_preference(order):
        """Creates a preference for checkout pro (Credit Card, etc)."""
        sdk = PaymentService.get_sdk()
        
        items = []
        for item in order.items:
            items.append({
                "title": item.product.name,
                "quantity": item.quantity,
                "unit_price": float(item.price_at_time)
            })
            
        # Add shipping as an item
        shipping_cost = float(order.total_amount) - sum(float(i.price_at_time * i.quantity) for i in order.items)
        if shipping_cost > 0:
            items.append({
                "title": "Frete",
                "quantity": 1,
                "unit_price": shipping_cost
            })

        preference_data = {
            "items": items,
            "payer": {
                "email": order.user.email
            },
            "back_urls": {
                "success": f"{current_app.config.get('BASE_URL', '')}/checkout/success/{order.id}",
                "failure": f"{current_app.config.get('BASE_URL', '')}/checkout/failure",
                "pending": f"{current_app.config.get('BASE_URL', '')}/checkout/pending"
            },
            "auto_return": "approved",
            "notification_url": current_app.config['WEBHOOK_URL'],
            "external_reference": str(order.id)
        }
        
        preference_response = sdk.preference().create(preference_data)
        return preference_response["response"]

    @staticmethod
    def process_webhook(data):
        sdk = PaymentService.get_sdk()
        
        if data.get("type") == "payment":
            payment_id = data.get("data", {}).get("id")
            payment_info = sdk.payment().get(payment_id)
            
            if payment_info["status"] == 200:
                payment_response = payment_info["response"]
                order_id = payment_response.get("external_reference")
                status = payment_response.get("status")
                
                if order_id:
                    order = Order.query.get(int(order_id))
                    if order:
                        if status == "approved":
                            order.status = "paid"
                        elif status == "cancelled":
                            order.status = "cancelled"
                        elif status == "in_process":
                            order.status = "pending"
                        
                        db.session.commit()
                        return True
        return False
