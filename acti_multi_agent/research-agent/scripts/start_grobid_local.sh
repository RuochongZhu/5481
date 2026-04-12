#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GROBID_DIR="${GROBID_DIR:-$ROOT_DIR/../grobid}"
DEFAULT_JAVA_HOME="$ROOT_DIR/.tools/jdk/jdk-21.0.10+7/Contents/Home"

if [ -z "${JAVA_HOME:-}" ]; then
  export JAVA_HOME="$DEFAULT_JAVA_HOME"
fi
export PATH="$JAVA_HOME/bin:$PATH"

if [ ! -x "$JAVA_HOME/bin/java" ]; then
  echo "JAVA_HOME is not usable: $JAVA_HOME" >&2
  echo "Expected local JDK at: $DEFAULT_JAVA_HOME" >&2
  exit 1
fi

if [ ! -d "$GROBID_DIR" ]; then
  echo "GROBID directory not found: $GROBID_DIR" >&2
  exit 1
fi

LOCAL_FONTCONFIG="$ROOT_DIR/.tools/grobid-libs/lib/libfontconfig.1.dylib"
FONTCONFIG_LIB="/opt/homebrew/opt/fontconfig/lib/libfontconfig.1.dylib"
if [ -f "$LOCAL_FONTCONFIG" ]; then
  export DYLD_FALLBACK_LIBRARY_PATH="$(dirname "$LOCAL_FONTCONFIG"):${DYLD_FALLBACK_LIBRARY_PATH:-}"
  echo "Using project-local fontconfig from: $LOCAL_FONTCONFIG"
elif [ ! -f "$FONTCONFIG_LIB" ]; then
  ALT_FONTCONFIG="$(find /usr/local /opt/homebrew "$HOME" -name 'libfontconfig.1.dylib' 2>/dev/null | head -1 || true)"
  if [ -n "$ALT_FONTCONFIG" ]; then
    export DYLD_FALLBACK_LIBRARY_PATH="$(dirname "$ALT_FONTCONFIG"):${DYLD_FALLBACK_LIBRARY_PATH:-}"
    echo "Using fontconfig from: $ALT_FONTCONFIG"
  else
    echo "Warning: libfontconfig.1.dylib not found. GROBID may start but pdfalto parsing can fail." >&2
  fi
fi

cd "$GROBID_DIR"
exec ./gradlew grobid-service:run
