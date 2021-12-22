#!/bin/bash

cd async-coordinator && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../async-function-sequence && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../client-side-scheduling && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../compiled-sequence && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../coordinator && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../event-sourcing && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../message-queue-based && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../routing-slip && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../storage-based && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../sync-function-sequence && sam build --cached --beta-features && sam deploy --no-confirm-changeset && \
cd ../workflow-engine && sam build --cached --beta-features && sam deploy --no-confirm-changeset


