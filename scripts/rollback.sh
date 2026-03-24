#!/usr/bin/env bash
# rollback.sh — Emergency Helm rollback
set -euo pipefail

NAMESPACE="${NAMESPACE:-production}"
REVISION="${1:-}"

echo "  Rolling back myapp in namespace: ${NAMESPACE}"

if [[ -z "$REVISION" ]]; then
  echo "   Rolling back to previous revision"
  helm rollback myapp -n "${NAMESPACE}" --wait
else
  echo "   Rolling back to revision: ${REVISION}"
  helm rollback myapp "${REVISION}" -n "${NAMESPACE}" --wait
fi

echo " Rollback complete"
helm history myapp -n "${NAMESPACE}" | tail -5
kubectl get pods -n "${NAMESPACE}"
