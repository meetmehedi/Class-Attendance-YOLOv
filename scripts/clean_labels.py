
import os
import sys

def get_image_path_from_label(label_path, image_dir):
    base = os.path.splitext(os.path.basename(label_path))[0]
    for ext in ['.jpg', '.jpeg', '.png']:
        img_path = os.path.join(image_dir, base + ext)
        if os.path.exists(img_path):
            return img_path
    return None

def clean_dataset(labels_dir, images_dir):
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    deleted_labels = 0
    deleted_images = 0
    fixed_class_ids = 0

    for label_file in label_files:
        label_path = os.path.join(labels_dir, label_file)
        
        # Remove empty labels + corresponding images
        if os.path.getsize(label_path) == 0:
            os.remove(label_path)
            deleted_labels += 1
            img_path = get_image_path_from_label(label_path, images_dir)
            if img_path and os.path.exists(img_path):
                os.remove(img_path)
                deleted_images += 1
            continue

        # Fix class IDs: ensure all = 0
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        modified = False
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                if parts[0] != '0':
                    parts[0] = '0'
                    modified = True
                new_lines.append(' '.join(parts) + '\n')
        
        if modified:
            with open(label_path, 'w') as f:
                f.writelines(new_lines)
            fixed_class_ids += 1

    print(f"[clean_labels.py] Deleted {deleted_labels} empty labels and {deleted_images} images.")
    print(f"[clean_labels.py] Fixed class IDs in {fixed_class_ids} label files.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_labels.py <labels_dir> <images_dir>")
        sys.exit(1)
    
    labels_dir = sys.argv[1]
    images_dir = sys.argv[2]
    clean_dataset(labels_dir, images_dir)
