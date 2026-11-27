#!/usr/bin/env python3
"""Inventory numeric owners in a tagged OCI layout without extracting files."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import tarfile

INDEX = "application/vnd.oci.image.index.v1+json"
MANIFEST = "application/vnd.oci.image.manifest.v1+json"
LAYER = "application/vnd.oci.image.layer.v1.tar"


def audit(layout: Path, tag: str) -> Counter:
    counts = Counter()
    seen = set()
    layer_count = 0

    def blob(descriptor):
        digest = descriptor["digest"]
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
            raise ValueError(f"unsupported blob digest: {digest!r}")
        path = layout / "blobs" / "sha256" / digest.split(":")[1]
        with path.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != digest.split(":")[1]:
                raise ValueError(f"blob digest mismatch: {digest}")
        return path

    def visit(descriptor):
        nonlocal layer_count
        if descriptor.get("annotations", {}).get("vnd.docker.reference.type") == "attestation-manifest":
            return
        digest = descriptor["digest"]
        media = descriptor["mediaType"]
        key = (digest, media)
        if key in seen:
            return
        seen.add(key)
        path = blob(descriptor)
        if media in (INDEX, MANIFEST):
            document = json.loads(path.read_text())
            children = document["manifests" if media == INDEX else "layers"]
            if not children:
                raise ValueError(f"empty {media}: {digest}")
            for child in children:
                visit(child)
        elif media in (LAYER, LAYER + "+gzip"):
            try:
                with tarfile.open(path, mode="r:gz" if media.endswith("+gzip") else "r:") as archive:
                    for member in archive:
                        if member.isfile():
                            with archive.extractfile(member) as content:
                                while content.read(1024 * 1024):
                                    pass
                        counts[(member.uid, member.gid)] += 1
            except (OSError, EOFError, tarfile.TarError) as exc:
                raise ValueError(f"cannot read layer {digest}: {exc}") from exc
            layer_count += 1
        else:
            raise ValueError(f"unsupported media type {media!r} in {digest}")

    index = json.loads((layout / "index.json").read_text())
    matches = [d for d in index["manifests"]
               if d.get("annotations", {}).get("org.opencontainers.image.ref.name") == tag]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one descriptor for tag {tag!r}, found {len(matches)}")
    visit(matches[0])
    if not layer_count:
        raise ValueError("no filesystem layers audited")
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("layout", type=Path)
    parser.add_argument("tag")
    args = parser.parse_args()
    try:
        counts = audit(args.layout, args.tag)
    except (OSError, ValueError, KeyError, TypeError, EOFError, tarfile.TarError) as exc:
        print(f"ownership audit failed: {exc}", file=sys.stderr)
        return 1
    for (uid, gid), count in sorted(counts.items()):
        print(f"{count:8d} {uid}/{gid}")
    if any(owner not in {(0, 0), (1000, 1000)} for owner in counts):
        print("ownership audit failed: unexpected numeric owner", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
