#!/usr/bin/env bash
# deploy.sh — Manual Helm deployment helper
set -euo pipefail

NAMESPACE="${NAMESPACE:-staging}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
VALUES_OVERRIDE="k8s/overlays/${NAMESPACE}/values-override.yaml"

echo "🚀 Deploying myapp to namespace: ${NAMESPACE}"
echo "   Image tag: ${IMAGE_TAG}"

helm upgrade --install myapp ./helm/myapp \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  --values helm/myapp/values.yaml \
  --values "${VALUES_OVERRIDE}" \
  --set api.image.tag="${IMAGE_TAG}" \
  --set worker.image.tag="${IMAGE_TAG}" \
  --atomic \
  --timeout 5m \
  --wait

echo "✅ Deployment complete"
kubectl get pods -n "${NAMESPACE}"
