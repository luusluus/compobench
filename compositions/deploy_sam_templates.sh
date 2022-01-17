#!/bin/bash

cd async_coordinator && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../async_function_sequence && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../compiled_sequence && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../client_side_scheduling && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../coordinator && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../event_sourcing && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../message_queue_based && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../routing_slip && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../blackboard_based && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../storage_based && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../function_sequence && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../workflow_engine && sam build --cached --beta-features && sam deploy --no-confirm-changeset


