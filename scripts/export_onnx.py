
import sys
from ultralytics import YOLO

def export_to_onnx(model_path, imgsz=416):
    model = YOLO(model_path)
    onnx_file = model.export(
        format='onnx',
        imgsz=imgsz,
        dynamic=False,
        simplify=True
    )
    print(f"[export_onnx.py] ONNX model saved to: {onnx_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_onnx.py <model.pt> [imgsz=416]")
        sys.exit(1)
    
    model_path = sys.argv[1]
    imgsz = int(sys.argv[2]) if len(sys.argv) > 2 else 416
    export_to_onnx(model_path, imgsz)
