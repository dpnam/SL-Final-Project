import os
import re
import json

detections_count_pattern = re.compile(r"detections_count = (\d+)")
unique_truth_count_pattern = re.compile(r"unique_truth_count = (\d+)")

class_pattern = re.compile(
    r"class_id = (?P<id>\d+), name = (?P<name>\w+), ap = (?P<ap>.*?)% .*?\(TP = (?P<tp>\d+), FP = (?P<fp>\d+)\)"
)

precision_recall_pattern = re.compile(
    r"precision = (?P<precision>\d+(\.\d+)?|-?nan), recall = (?P<recall>\d+(\.\d+)?|-?nan), F1-score = (?P<f1_score>\d+(\.\d+)?|-?nan)"
)

tp_fp_fn_iou_pattern = re.compile(
    r"TP = (?P<tp>\d+), FP = (?P<fp>\d+), FN = (?P<fn>\d+), average IoU = (?P<iou>\d+(\.\d+)?)"
)

map_pattern = re.compile(r"\(mAP@0.50\) = (\d+(\.\d+)?)")

_, dirs, _ = next(os.walk("."))

for dir in dirs:
    _, mapsets, _ = next(os.walk(dir))
    for mapset in mapsets:
        containing_dir = os.path.join(dir, mapset)
        _, _, files = next(os.walk(containing_dir))
        data = []
        for filename in files:
            iteration = int(filename.replace("mAP_", "").replace(".txt", ""))
            print(filename, iteration)
            classes = []
            with open(os.path.join(containing_dir, filename)) as f:
                file_content = f.read()
                detections_count = int(
                    detections_count_pattern.search(file_content).group(1)
                )

                unique_truth_count = int(
                    unique_truth_count_pattern.search(file_content).group(1)
                )

                for class_data in class_pattern.finditer(file_content):
                    d = class_data.groupdict()
                    d["id"] = int(d["id"])
                    d["ap"] = float(d["ap"])
                    d["tp"] = int(d["tp"])
                    d["fp"] = int(d["fp"])
                    classes.append(d)

                precision_data = precision_recall_pattern.search(file_content)
                d = precision_data.groupdict()
                precision = float(d["precision"])
                recall = float(d["recall"])
                f1_score = float(d["f1_score"])

                tp_data = tp_fp_fn_iou_pattern.search(file_content)
                d = tp_data.groupdict()
                tp = int(d["tp"])
                fp = int(d["fp"])
                fn = int(d["fn"])
                avg_iou = float(d["iou"])

                map = float(map_pattern.search(file_content).group(1))

            data.append(
                {
                    "iteration": iteration,
                    "detections_count": detections_count,
                    "unique_truth_count": unique_truth_count,
                    "classes": classes,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1_score,
                    "tp": tp,
                    "fp": fp,
                    "fn": fn,
                    "avg_iou": avg_iou,
                    "map": map,
                }
            )
        data.sort(key=lambda x: x["iteration"])
        with open(f"{dir}_{mapset}.json", "w") as f:
            json.dump(data, f, allow_nan=True, indent=2)
