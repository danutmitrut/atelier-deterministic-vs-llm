#!/usr/bin/env python3
"""
Generator de imagini pe kie.ai, pentru fundalurile de carusel.

Usage: python3 kie_generate.py <prompt> <output_path> [--aspect 4:5|1:1] [--timeout 180]

Cheia se ia din Keychain (serviciul „kie-api-key"). Scriptul nu citeste .env,
nu scrie .env si nu trimite imaginea nicaieri in afara: singurul lui rezultat
e fisierul de pe disc. Publicarea e treaba Publisher-ului, dupa aprobarea omului.
"""

import json
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

KIE_KEY = os.environ.get("KIE_API_KEY", "")
if not KIE_KEY:
    # Fallback: read from macOS Keychain (seif), service "kie-api-key"
    try:
        import subprocess
        KIE_KEY = subprocess.run(
            ["security", "find-generic-password", "-a", os.environ.get("USER", ""), "-s", "kie-api-key", "-w"],
            capture_output=True, text=True,
        ).stdout.strip()
    except Exception:
        pass
BASE = "https://api.kie.ai/api/v1"


def post_json(url, body, key):
    req = Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    return json.loads(urlopen(req).read())


def get_json(url, key):
    req = Request(url, headers={"Authorization": f"Bearer {key}"})
    return json.loads(urlopen(req).read())


def create_task(prompt, aspect="1:1", input_image_url=None):
    inp = {"prompt": prompt, "aspect_ratio": aspect}
    if input_image_url:
        inp["image_url"] = input_image_url
    body = {"model": "gpt-image-2-image-to-image", "input": inp}
    resp = post_json(f"{BASE}/jobs/createTask", body, KIE_KEY)
    if resp.get("code") != 200:
        raise RuntimeError(f"createTask failed: {resp}")
    return resp["data"]["taskId"]


def poll_until_done(task_id, timeout_s=180, interval=6):
    deadline = time.time() + timeout_s
    last_state = None
    while time.time() < deadline:
        resp = get_json(f"{BASE}/jobs/recordInfo?taskId={task_id}", KIE_KEY)
        data = resp.get("data", {})
        state = data.get("state")
        if state != last_state:
            print(f"  [{task_id[:8]}] state={state}", file=sys.stderr)
            last_state = state
        if state == "success":
            result = json.loads(data.get("resultJson", "{}"))
            urls = result.get("resultUrls", [])
            if not urls:
                raise RuntimeError(f"success but no resultUrls: {data}")
            return urls[0], data.get("costTime"), data.get("creditsConsumed")
        if state in ("failed", "error"):
            raise RuntimeError(f"task failed: {data}")
        time.sleep(interval)
    raise TimeoutError(f"task {task_id} timed out after {timeout_s}s")


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    with urlopen(req) as r, open(dest, "wb") as f:
        f.write(r.read())
    return os.path.getsize(dest)


def generate(prompt, output_path, aspect="1:1", timeout_s=180, input_image_url=None):
    print(f"-> Generating: {output_path}", file=sys.stderr)
    print(f"   Prompt: {prompt[:120]}...", file=sys.stderr)
    if input_image_url:
        print(f"   Input image: {input_image_url[:80]}...", file=sys.stderr)
    task_id = create_task(prompt, aspect, input_image_url)
    print(f"   taskId={task_id}", file=sys.stderr)
    image_url, cost_time, credits = poll_until_done(task_id, timeout_s)
    size = download(image_url, output_path)
    print(
        f"   OK: {output_path} ({size//1024}KB, {cost_time}s, {credits} credits)",
        file=sys.stderr,
    )
    return {
        "task_id": task_id,
        "output_path": output_path,
        "image_url": image_url,
        "cost_time_s": cost_time,
        "credits": credits,
        "size_bytes": size,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 kie_generate.py <prompt> <output_path> "
              "[--aspect 4:5|1:1] [--input-url <url>] [--timeout 180]", file=sys.stderr)
        sys.exit(1)
    prompt = sys.argv[1]
    output_path = sys.argv[2]
    input_url = None
    aspect = "4:5"  # formatul caruselelor; 1:1 se cere explicit
    timeout_s = 180
    if "--aspect" in sys.argv:
        aspect = sys.argv[sys.argv.index("--aspect") + 1]
    if "--input-url" in sys.argv:
        input_url = sys.argv[sys.argv.index("--input-url") + 1]
    if "--timeout" in sys.argv:
        timeout_s = int(sys.argv[sys.argv.index("--timeout") + 1])
    result = generate(prompt, output_path, aspect=aspect,
                      input_image_url=input_url, timeout_s=timeout_s)
    print(json.dumps(result, indent=2))
