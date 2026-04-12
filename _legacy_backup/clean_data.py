import os
import cv2
import argparse
import shutil

def clean_data(input_dir, output_dir):
    allowed_labels = {'happy', 'sad', 'neutral', 'angry', 'disgust', 'fear'}
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                
                # Determine label from directory name
                label = os.path.basename(root).lower()
                
                if label in allowed_labels:
                    # Create label directory in output if it doesn't exist
                    label_out_dir = os.path.join(output_dir, label)
                    if not os.path.exists(label_out_dir):
                        os.makedirs(label_out_dir)
                    
                    try:
                        img = cv2.imread(file_path)
                        if img is not None:
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            resized = cv2.resize(gray, (48, 48))
                            
                            output_path = os.path.join(label_out_dir, file)
                            cv2.imwrite(output_path, resized)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess image data.")
    parser.add_argument("--input_dir", type=str, required=True, help="Path to the input directory containing labeled folders.")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to the output directory.")
    
    args = parser.parse_args()
    clean_data(args.input_dir, args.output_dir)
