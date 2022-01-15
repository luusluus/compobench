#!/bin/bash

cd async_coordinator && sam delete --no-prompts && \
cd ../async_function_sequence && sam delete --no-prompts && \
cd ../compiled_sequence && sam delete --no-prompts && \
cd ../client_side_scheduling && sam delete --no-prompts && \
cd ../coordinator && sam delete --no-prompts && \
cd ../event_sourcing && sam delete --no-prompts && \
cd ../message_queue-based && sam delete --no-prompts && \
cd ../routing_slip && sam delete --no-prompts && \
cd ../blackboard_based && sam delete --no-prompts && \
cd ../storage_based && sam delete --no-prompts && \
cd ../function_sequence && sam delete --no-prompts && \
cd ../workflow_engine && sam delete --no-prompts 


