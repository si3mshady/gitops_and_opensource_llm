#!/bin/bash

# Set the age threshold in days
AGE_THRESHOLD=4

# Get the current date
CURRENT_DATE=$(date +%s)

# Loop through all namespaces
for namespace in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
    # Get the creation timestamp of the namespace
    CREATION_TIMESTAMP=$(kubectl get namespace "$namespace" -o jsonpath='{.metadata.creationTimestamp}')

    # Convert the creation timestamp to seconds
    CREATION_DATE=$(date -d "$CREATION_TIMESTAMP" +%s)

    # Calculate the age of the namespace in seconds
    AGE_SECONDS=$((CURRENT_DATE - CREATION_DATE))
    AGE_DAYS=$((AGE_SECONDS / 86400))

    # Delete the namespace if it's less than the age threshold
    if [ "$AGE_DAYS" -lt "$AGE_THRESHOLD" ]; then
        echo "Deleting namespace '$namespace' (age: $AGE_DAYS days)"
        kubectl delete namespace "$namespace"
    fi
done