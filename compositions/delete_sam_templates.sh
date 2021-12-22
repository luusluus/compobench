#!/bin/bash

cd async-coordinator && sam delete --no-prompts && \
cd ../async-function-sequence && sam delete --no-prompts && \
cd ../client-side-scheduling && sam delete --no-prompts && \
cd ../compiled-sequence && sam delete --no-prompts && \
cd ../coordinator && sam delete --no-prompts && \
cd ../event-sourcing && sam delete --no-prompts && \
cd ../message-queue-based && sam delete --no-prompts && \
cd ../routing-slip && sam delete --no-prompts && \
cd ../storage-based && sam delete --no-prompts && \
cd ../sync-function-sequence && sam delete --no-prompts && \
cd ../workflow-engine && sam delete --no-prompts 


