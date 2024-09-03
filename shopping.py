import asyncio
import logging
from typing import Any

import littlehorse
from littlehorse.config import LHConfig
from littlehorse.worker import WorkerContext, LHTaskWorker 

logging.basicConfig(level=logging.INFO)
async def create_order(order: dict[str, Any]):
    order['total_cost']
    print(order['total_cost'])

async def check_stock(order_items: list[Any]):
    print(order_items)

async def collect_payment(customer: str, payment: float):
    print(payment)

async def send_email():
    print("send an email")

async def change_order_status():
    print("change the status for the order")

async def schedule_delivery():
    print("delivery")

async def assign_courier():
    print("courier")

async def update_shipping_details():
    print("update shipping")

async def complete_order(order_id: str):
    print("complete")

async def main() -> None:
    logging.info("Starting Task Worker!")
    
    # Configuration loaded from environment variables
    config = LHConfig()
    create_order_worker = LHTaskWorker(create_order, "create-order", config)
    create_order_worker.register_task_def()

    check_stock_worker = LHTaskWorker(check_stock, "check-stock", config)
    check_stock_worker.register_task_def()
    

    collect_payment_worker = LHTaskWorker(collect_payment, "collect-payment", config)
    collect_payment_worker. register_task_def()
     

    send_email_worker = LHTaskWorker(send_email, "send-email", config)
    send_email_worker.register_task_def()
     

    change_order_status_worker = LHTaskWorker(change_order_status, "change-order-status", config)
    change_order_status_worker.register_task_def()
    

    schedule_delivery_worker = LHTaskWorker(schedule_delivery, "schedule-delivery", config)
    schedule_delivery_worker.register_task_def()
    

    assign_courier_worker = LHTaskWorker(assign_courier, "assign-courier", config)
    assign_courier_worker.register_task_def()
    

    update_shipping_details_worker = LHTaskWorker(update_shipping_details, "update-shipping-details", config)
    update_shipping_details_worker.register_task_def()
    

    complete_order_worker = LHTaskWorker(complete_order, "complete-order", config)
    complete_order_worker.register_task_def()

    await asyncio.gather(littlehorse.start(create_order_worker), littlehorse.start(check_stock_worker), littlehorse.start(collect_payment_worker), 
           littlehorse.start(send_email_worker), littlehorse.start(change_order_status_worker), 
           littlehorse.start(schedule_delivery_worker), littlehorse.start(assign_courier_worker), 
           littlehorse.start(update_shipping_details_worker), littlehorse.start(complete_order_worker))


if __name__ == '__main__':
    asyncio.run(main()) 

