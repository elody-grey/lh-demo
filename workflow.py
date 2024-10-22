import logging

import littlehorse
from littlehorse.config import LHConfig
from littlehorse.model.common_enums_pb2 import VariableType
from littlehorse.model import VariableMutationType

from littlehorse.workflow import Workflow, WorkflowThread, SpawnedThreads, Comparator

logging.basicConfig(level=logging.INFO)


# The logic for our WfSpec (worfklow) lives in this function!
def get_workflow() -> Workflow:

    def send_email(wf: WorkflowThread) -> None:
        wf.execute("send-email") 
    
    def change_order_status (wf: WorkflowThread) -> None: 
        wf.execute("change-order-status")
    
    def schedule_delivery (wf:WorkflowThread) -> None:
        wf.execute("schedule-delivery")
        wf.execute("assign-courier") 
        wf.execute("update-shipping-details")
    

    def request_stock(wf:WorkflowThread) -> None:
        check_stock_output = wf.assign_user_task("check-stock", user_group="warehouse")
        is_available = wf.add_variable("is-available", VariableType.BOOL)
        wf.mutate(is_available, VariableMutationType.ASSIGN, check_stock_output.with_json_path("$.InventoryAvailability"))
        
        def fail(wf: WorkflowThread) -> None:
            wf.fail("no-inventory", "No Inventory")
        
        wf.do_if(wf.condition(is_available, Comparator.EQUALS, False), fail)
    

    def wait_for_payment(wf:WorkflowThread) -> None:
        check_payment_output = wf.assign_user_task("wait-for-payment", user_group="customer service")
        confirmation_number = wf.add_variable("confirmation-number", VariableType.STR)
        wf.mutate(confirmation_number, VariableMutationType.ASSIGN, check_payment_output.with_json_path("$.ConfirmationNumber"))

        def fail(wf: WorkflowThread) -> None:
            wf.fail("not-enough-money", "Not enough balance")
        
        wf.do_if(wf.condition(confirmation_number, Comparator.EQUALS, None), fail)

    def shopping(wf: WorkflowThread) -> None:
        # Define an input variable
        order = wf.add_variable("order-input", VariableType.JSON_OBJ)
        items = wf.add_variable("order-items", VariableType.JSON_ARR)
        customer = wf.add_variable("customer-id", VariableType.STR)
        wf.mutate(items, VariableMutationType.ASSIGN, order.with_json_path("$.items"))
        wf.mutate(customer, VariableMutationType.ASSIGN, order.with_json_path("$.customer.id"))
        wf.execute("create-order", order)
        stocknode = wf.execute("check-stock", items)
        wf.handle_exception(stocknode, request_stock, "out-of-stock")
        
        paymentnode = wf.execute("collect-payment", customer, order.with_json_path("$.total_cost")) 
        wf.handle_exception(paymentnode, wait_for_payment, "payment-fail")
        
        send_email_thread = wf.spawn_thread(send_email, "send-email")
        change_order_status_thread = wf.spawn_thread(change_order_status, "change-order-status")
        schedule_delivery_thread = wf.spawn_thread(schedule_delivery, "schedule-delivery")
        wf.wait_for_threads(SpawnedThreads(fixed_threads=[send_email_thread, change_order_status_thread, schedule_delivery_thread]))
        wf.execute("complete-order", order.with_json_path("$.order_id"))

    # Provide the name of the WfSpec and a function which has the logic.
    return Workflow("shopping", shopping)


def main() -> None:
    logging.info("Registering WfSpec and TaskDef")

    # Configuration loaded from environment variables
    config = LHConfig()
    wf = get_workflow()


    littlehorse.create_workflow_spec(wf, config)


if __name__ == "__main__":
    main()
