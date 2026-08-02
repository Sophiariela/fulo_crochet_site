import logging
import mercadopago
from flask import current_app
from app.models.order import Order
from app import db

logger = logging.getLogger(__name__)


class PaymentService:
    """Integração oficial com o Mercado Pago Checkout Pro (SDK oficial)."""

    @staticmethod
    def get_sdk():
        token = current_app.config.get('MP_ACCESS_TOKEN')
        if not token or 'YOUR-ACCESS-TOKEN' in token:
            logger.error(
                "MP_ACCESS_TOKEN não configurado corretamente. "
                "Defina a variável de ambiente MP_ACCESS_TOKEN com um access token válido do Mercado Pago."
            )
        return mercadopago.SDK(token or "DUMMY_TOKEN")

    @staticmethod
    def create_preference(order):
        """Cria uma preferência de pagamento (Checkout Pro oficial) para o pedido informado.

        Retorna o dicionário de resposta da API do Mercado Pago (contendo, entre outros
        campos, 'id' e 'init_point') ou None em caso de falha.
        """
        sdk = PaymentService.get_sdk()

        items = []
        for item in order.items:
            items.append({
                "title": item.product.name,
                "quantity": item.quantity,
                "unit_price": float(item.price_at_time),
                "currency_id": "BRL",
            })

        # Frete como item adicional, se houver
        items_total = sum(float(i.price_at_time) * i.quantity for i in order.items)
        shipping_cost = float(order.total_amount) - items_total
        if shipping_cost > 0:
            items.append({
                "title": "Frete",
                "quantity": 1,
                "unit_price": round(shipping_cost, 2),
                "currency_id": "BRL",
            })

        base_url = current_app.config.get('BASE_URL', '').rstrip('/')
        preference_data = {
            "items": items,
            "payer": {
                "email": order.user.email
            },
            "back_urls": {
                "success": f"{base_url}/checkout/success",
                "failure": f"{base_url}/checkout/failure",
                "pending": f"{base_url}/checkout/pending",
            },
            "auto_return": "approved",
            "notification_url": current_app.config.get('WEBHOOK_URL'),
            "external_reference": str(order.id),
        }

        try:
            preference_response = sdk.preference().create(preference_data)
            response = preference_response.get("response", {})
            status = preference_response.get("status")

            if status not in (200, 201) or not response.get("init_point"):
                logger.error(
                    "Falha ao criar preferência no Mercado Pago para o pedido #%s. "
                    "Status HTTP: %s. Resposta: %s",
                    order.id, status, response
                )
                return None

            logger.info(
                "Preferência criada com sucesso para o pedido #%s. preference_id=%s init_point=%s",
                order.id, response.get("id"), response.get("init_point")
            )
            return response
        except Exception:
            logger.error(
                "Erro inesperado ao criar preferência no Mercado Pago para o pedido #%s",
                order.id, exc_info=True
            )
            return None

    @staticmethod
    def process_webhook(data):
        """Processa notificações do Mercado Pago (webhook) e atualiza o status do pedido."""
        sdk = PaymentService.get_sdk()

        if data.get("type") != "payment":
            logger.info("Notificação recebida com tipo não tratado: %s", data.get("type"))
            return False

        payment_id = data.get("data", {}).get("id")
        if not payment_id:
            logger.error("Notificação de pagamento recebida sem payment_id. Payload: %s", data)
            return False

        try:
            payment_info = sdk.payment().get(payment_id)
        except Exception:
            logger.error("Erro ao consultar pagamento %s no Mercado Pago", payment_id, exc_info=True)
            return False

        if payment_info.get("status") != 200:
            logger.error(
                "Falha ao consultar pagamento %s no Mercado Pago. Status: %s. Resposta: %s",
                payment_id, payment_info.get("status"), payment_info.get("response")
            )
            return False

        payment_response = payment_info["response"]
        order_id = payment_response.get("external_reference")
        status = payment_response.get("status")

        if not order_id:
            logger.error("Pagamento %s aprovado sem external_reference. Resposta: %s", payment_id, payment_response)
            return False

        order = Order.query.get(int(order_id))
        if not order:
            logger.error("Pedido #%s referenciado pelo pagamento %s não foi encontrado.", order_id, payment_id)
            return False

        if status == "approved":
            order.status = "paid"
        elif status == "cancelled" or status == "rejected":
            order.status = "cancelled"
        elif status == "in_process" or status == "pending":
            order.status = "pending"
        else:
            logger.info("Status de pagamento não mapeado '%s' para o pedido #%s.", status, order_id)

        db.session.commit()
        logger.info("Pedido #%s atualizado para status '%s' via webhook (payment_id=%s).", order_id, order.status, payment_id)
        return True
