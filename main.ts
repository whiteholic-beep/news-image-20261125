// news-image-20261125 — "THE WORLD ON ONE PAGE", Wednesday 25 November 2026.
//
// Node 22 entrypoint, standard library only. The repository ships the
// finished front page as entry.png (drawn by draw.py: 35 stories, all
// from Wednesday 25 November 2026, in the style of the previous day's
// rank-1 winner — three illustrated hero leads, eight secondary
// stories, a pin map, a 24-item ALSO list and a red DATE CHECK strip).
// This program copies that file into the output directory the grader
// provides and refuses to emit anything that would fail the gate.
//
// The page sums up Wednesday 25 November 2026: Ukrainian drones hit
// two Russian refineries 800 km deep, Asian stocks rout as KOSPI falls
// 6%, Shenzhou-24 carries the first foreign astronaut to Tiangong, the
// Odesa strike, the Cartagena supermarket siege, Australia's digital
// duty of care, the Hodeidah retaliation, the Hormuz shipping call,
// Indonesia's VP deadline, the Iowa explosives disposal and Xiamen's
// 50-jet Boeing order — plus 24 more stories in the ALSO list.
//
// No network, no randomness, no clock: both grader runs write exactly
// the same bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";

const PNG_SIG = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

// The digest of the front page this program is meant to ship. Pinning
// it here means a stale or accidentally regenerated entry.png fails
// loudly instead of going out as a different picture.
const EXPECTED_SHA256 =
  "34e391a2a3d23c7ea5366251d30008772cc61e4241007ac3483077f3dee446d6";

const sourcePath = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const targetPath = join(outDir, "entry.png");

function digest(bytes: Buffer): string {
  return createHash("sha256").update(bytes).digest("hex");
}

function abort(reason: string): never {
  throw new Error(`news-image-20261125: ${reason}`);
}

if (!existsSync(sourcePath)) {
  abort("entry.png is missing next to main.ts");
}
const image = readFileSync(sourcePath);
if (image.length === 0) {
  abort("entry.png is empty (0 bytes)");
}
if (!image.subarray(0, 8).equals(PNG_SIG)) {
  abort("entry.png is not a PNG file (bad signature bytes)");
}
if (image.length > MAX_BYTES) {
  abort(`entry.png is ${image.length} bytes, over the 1 MiB limit`);
}
if (digest(image) !== EXPECTED_SHA256) {
  abort(
    `entry.png digest ${digest(image)} does not match the pinned ` +
      `front page (${EXPECTED_SHA256}); regenerate it with draw.py`,
  );
}
// IHDR sits right after the 8-byte signature: a 4-byte length, the
// letters "IHDR", then width and height as big-endian uint32 values.
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  abort(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(dirname(targetPath), { recursive: true });
copyFileSync(sourcePath, targetPath);

// Read the copy back and compare it byte for byte with the source, so
// a truncated or altered write can never pass silently.
const emitted = readFileSync(targetPath);
if (!emitted.equals(image)) {
  abort("output differs from entry.png after copying");
}

console.log(
  `wrote ${targetPath} (${emitted.length} bytes, sha256 ${digest(emitted)})`,
);
