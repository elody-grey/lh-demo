import logging

import littlehorse
from littlehorse.config import LHConfig
from littlehorse.model.common_enums_pb2 import VariableType
from littlehorse.model import VariableMutationType

from littlehorse.workflow import Workflow, WorkflowThread, SpawnedThreads

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
    


    def shopping(wf: WorkflowThread) -> None:
        # Define an input variable
        order = wf.add_variable("order-input", VariableType.JSON_OBJ)
        items = wf.add_variable("order-items", VariableType.JSON_ARR)
        customer = wf.add_variable("customer-id", VariableType.STR)
        wf.mutate(items, VariableMutationType.ASSIGN, order.with_json_path("$.items"))
        wf.mutate(customer, VariableMutationType.ASSIGN, order.with_json_path("$.customer.id"))
        wf.execute("create-order", order)
        wf.execute("check-stock", items)
        wf.execute("collect-payment", customer, order.with_json_path("$.total_cost")) 
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

