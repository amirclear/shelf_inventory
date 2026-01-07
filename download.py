import os
import requests

FILES = [
    # Originals
    (
        "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/zidane.jpg",
        "static/samples/shelf1.jpg",
    ),
    (
        "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/bus.jpg",
        "static/samples/shelf3.jpg",
    ),

    # BBoxes (fake – MVP)
    (
        "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/zidane.jpg",
        "static/bboxes/shelf1_bbox.jpg",
    ),
    (
        "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/bus.jpg",
        "static/bboxes/shelf3_bbox.jpg",
    ),
]

def download(url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    print(f"Downloading:\n  {url}\n-> {out_path}")

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    with open(out_path, "wb") as f:
        f.write(r.content)

    print("OK\n")

def main():
    for url, path in FILES:
        download(url, path)

    print("✅ All demo images downloaded successfully.")

if __name__ == "__main__":
    main()
