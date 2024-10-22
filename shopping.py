import asyncio
import logging
from typing import Any

import littlehorse
from littlehorse.config import LHConfig
from littlehorse.worker import LHTaskWorker
from littlehorse.model.common_enums_pb2 import VariableType

from littlehorse.model import PutUserTaskDefRequest, UserTaskField
from littlehorse.exceptions import LHTaskException

logging.basicConfig(level=logging.INFO)

class ShoppingService:

    async def create_order(self, order: dict[str, Any]) -> None:
        print(order['total_cost'])

    async def check_stock(self, order_items: list[Any]) -> None:
        for item in order_items:
            print(item['quantity'])
            if item['quantity'] > 500:
                raise LHTaskException('out-of-stock', "not enough inventory")

    async def collect_payment(self, customer: str, payment: float) -> None:
        if payment > 100:
            raise LHTaskException('payment-failure', 'need more money')
        print(payment)

    async def send_email(self) -> None:
        print("send an email")

    async def change_order_status(self) -> None:
        print("change the status for the order")

    async def schedule_delivery(self) -> None:
        print("delivery")

    async def assign_courier(self) -> None:
        print("courier")

    async def update_shipping_details(self) -> None:
        print("update shipping")

    async def complete_order(self, order_id: str) -> None:
        print(order_id)

    async def get_user_task_def(self):
        return PutUserTaskDefRequest(
        name="check-stock",
        fields=[
            UserTaskField(
                name="InventoryAvailability",
                description="Is inventory avaiable?",
                display_name="Available?",
                required=True,
                type=VariableType.BOOL
            )
        ]
    )

    async def notify_customer(self) -> None:
        print("notify_customer")

    def get_user_task_payment(self):
        return PutUserTaskDefRequest(
            name="wait-for-payment",
            fields=[
                UserTaskField(
                    name="ConfirmationNumber",
                    description="Is there enough money?",
                    display_name="Money balance",
                    required=True,
                    type=VariableType.BOOL
                )
            ]
        )
    
    

async def main() -> None:
    logging.info("Starting Task Worker!")
    
    # Configuration loaded from environment variables
    config = LHConfig()
    service = ShoppingService()
    create_order_worker = LHTaskWorker(service.create_order, "create-order", config)
    create_order_worker.register_task_def()

    check_stock_worker = LHTaskWorker(service.check_stock, "check-stock", config)
    check_stock_worker.register_task_def()
    

    collect_payment_worker = LHTaskWorker(service.collect_payment, "collect-payment", config)
    collect_payment_worker.register_task_def()
    

    send_email_worker = LHTaskWorker(service.send_email, "send-email", config)
    send_email_worker.register_task_def()
     

    change_order_status_worker = LHTaskWorker(service.change_order_status, "change-order-status", config)
    change_order_status_worker.register_task_def()
    

    schedule_delivery_worker = LHTaskWorker(service.schedule_delivery, "schedule-delivery", config)
    schedule_delivery_worker.register_task_def()
    

    assign_courier_worker = LHTaskWorker(service.assign_courier, "assign-courier", config)
    assign_courier_worker.register_task_def()
    

    update_shipping_details_worker = LHTaskWorker(service.update_shipping_details, "update-shipping-details", config)
    update_shipping_details_worker.register_task_def()
    

    complete_order_worker = LHTaskWorker(service.complete_order, "complete-order", config)
    complete_order_worker.register_task_def()

    client = config.stub()
    put_user_task = service.get_user_task_def()
    client.PutUserTaskDef(put_user_task)

    client.PutUserTaskDef(service.get_user_task_payment())

    tasks = [
        create_order_worker,
        check_stock_worker,
        collect_payment_worker,
        send_email_worker,
        change_order_status_worker,
        schedule_delivery_worker,
        assign_courier_worker,
        update_shipping_details_worker,
        complete_order_worker
    ]

    await littlehorse.start(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
