#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../flutter_app"
exec flutter run -d chrome
