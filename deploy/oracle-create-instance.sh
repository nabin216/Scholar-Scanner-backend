#!/bin/bash
# Create an Always Free Ampere A1 instance on Oracle Cloud, retrying until capacity is available.
# Run inside OCI Cloud Shell (CLI is preinstalled and authenticated):
#   bash oracle-create-instance.sh

set -uo pipefail

# ---- Settings (Always Free limit: 4 OCPU / 24 GB total, 200 GB storage total) ----
INSTANCE_NAME="${INSTANCE_NAME:-scholarship-backend}"
SHAPE="${SHAPE:-VM.Standard.A1.Flex}"   # or VM.Standard.E2.1.Micro (x86, 1 GB RAM)
OCPUS="${OCPUS:-2}"
MEMORY_GB="${MEMORY_GB:-12}"
BOOT_GB="${BOOT_GB:-50}"
UBUNTU_VERSION="${UBUNTU_VERSION:-22.04}"
RETRY_SECONDS="${RETRY_SECONDS:-60}"
COMPARTMENT_ID="${COMPARTMENT_ID:-${OCI_TENANCY:-}}"
SSH_KEY_FILE="${SSH_KEY_FILE:-$HOME/.ssh/oracle-key.pub}"

if [ -z "$COMPARTMENT_ID" ]; then
    echo "COMPARTMENT_ID not set. Run: export COMPARTMENT_ID=<your tenancy OCID>"
    exit 1
fi

# ---- SSH key: use an existing public key, or generate one ----
if [ ! -f "$SSH_KEY_FILE" ]; then
    echo "No public key at $SSH_KEY_FILE - generating a new key pair..."
    mkdir -p "$HOME/.ssh"
    ssh-keygen -t rsa -b 4096 -N "" -f "${SSH_KEY_FILE%.pub}"
    echo "Download ${SSH_KEY_FILE%.pub} from Cloud Shell (menu > Download) to SSH in later."
fi

# ---- Don't create a duplicate ----
EXISTING=$(oci compute instance list --compartment-id "$COMPARTMENT_ID" \
    --display-name "$INSTANCE_NAME" --lifecycle-state RUNNING \
    --query 'data[0].id' --raw-output 2>/dev/null)
if [ -n "$EXISTING" ] && [ "$EXISTING" != "null" ]; then
    echo "Instance '$INSTANCE_NAME' already running: $EXISTING"
    exit 0
fi

# ---- Find a public subnet ----
SUBNET_ID="${SUBNET_ID:-$(oci network subnet list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[?"prohibit-public-ip-on-vnic"==`false`] | [0].id' --raw-output 2>/dev/null)}"
if [ -z "$SUBNET_ID" ] || [ "$SUBNET_ID" == "null" ]; then
    echo "No public subnet found. Create one first:"
    echo "  Networking > Virtual Cloud Networks > Start VCN Wizard > 'Create VCN with Internet Connectivity'"
    exit 1
fi

# ---- Latest Ubuntu image for ARM ----
IMAGE_ID=$(oci compute image list --compartment-id "$COMPARTMENT_ID" \
    --operating-system "Canonical Ubuntu" --operating-system-version "$UBUNTU_VERSION" \
    --shape "$SHAPE" --sort-by TIMECREATED --sort-order DESC \
    --query 'data[0].id' --raw-output)
if [ -z "$IMAGE_ID" ] || [ "$IMAGE_ID" == "null" ]; then
    echo "Could not find an Ubuntu $UBUNTU_VERSION image for $SHAPE"
    exit 1
fi

# Only Flex shapes take an OCPU/memory config
SHAPE_CONFIG_ARGS=()
if [[ "$SHAPE" == *Flex ]]; then
    SHAPE_CONFIG_ARGS=(--shape-config "{\"ocpus\": $OCPUS, \"memoryInGBs\": $MEMORY_GB}")
fi

ADS=$(oci iam availability-domain list --compartment-id "$COMPARTMENT_ID" \
    --query 'data[].name' --raw-output | jq -r '.[]')

echo "Subnet: $SUBNET_ID"
echo "Image:  $IMAGE_ID"
echo "Shape:  $SHAPE ($OCPUS OCPU, $MEMORY_GB GB RAM, $BOOT_GB GB disk)"
echo "Trying availability domains: $(echo $ADS)"
echo "Press Ctrl+C to stop."

ATTEMPT=0
while true; do
    for AD in $ADS; do
        ATTEMPT=$((ATTEMPT + 1))
        echo "[$(date '+%H:%M:%S')] Attempt $ATTEMPT in $AD..."

        OUTPUT=$(oci compute instance launch \
            --availability-domain "$AD" \
            --compartment-id "$COMPARTMENT_ID" \
            --display-name "$INSTANCE_NAME" \
            --shape "$SHAPE" \
            "${SHAPE_CONFIG_ARGS[@]}" \
            --image-id "$IMAGE_ID" \
            --subnet-id "$SUBNET_ID" \
            --assign-public-ip true \
            --boot-volume-size-in-gbs "$BOOT_GB" \
            --ssh-authorized-keys-file "$SSH_KEY_FILE" \
            --wait-for-state RUNNING 2>&1)

        if echo "$OUTPUT" | grep -q '"lifecycle-state": "RUNNING"'; then
            INSTANCE_ID=$(echo "$OUTPUT" | grep -o '"id": "ocid1.instance[^"]*"' | head -1 | cut -d'"' -f4)
            PUBLIC_IP=$(oci compute instance list-vnics --instance-id "$INSTANCE_ID" \
                --query 'data[0]."public-ip"' --raw-output)
            echo ""
            echo "SUCCESS! Instance created in $AD"
            echo "Instance ID: $INSTANCE_ID"
            echo "Public IP:   $PUBLIC_IP"
            echo "Connect:     ssh -i oracle-key ubuntu@$PUBLIC_IP"
            exit 0
        elif echo "$OUTPUT" | grep -qi "capacity"; then
            echo "  Out of capacity."
        elif echo "$OUTPUT" | grep -qi "TooManyRequests"; then
            echo "  Rate limited - waiting longer."
            sleep 120
        elif echo "$OUTPUT" | grep -qi "LimitExceeded"; then
            echo "  Free tier limit exceeded - you may already have A1 instances using your 4 OCPU / 24 GB."
            echo "$OUTPUT"
            exit 1
        else
            echo "  Unexpected error:"
            echo "$OUTPUT"
            exit 1
        fi
    done
    echo "Waiting $RETRY_SECONDS seconds before the next round..."
    sleep "$RETRY_SECONDS"
done
