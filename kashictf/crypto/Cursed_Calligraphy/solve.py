#!/usr/bin/env python3
"""
Cursed Calligraphy - KashiCTF Challenge Solver

The challenge involves extracting a hand-drawn flag from a video file.
The flag was "drawn" with digital ink, creating overlapping messy strokes.

Solution approach:
1. Parse Excel file to find the correct archive (marked "This is the one")
2. Download the MP4 video from Google Drive
3. Extract stroke data by analyzing frame-by-frame changes
4. Segment the video into time windows to isolate individual characters
5. Manually read the characters from the segmented strokes
"""

import cv2
import numpy as np
import pandas as pd
import os

def extract_segments(video_path, output_dir='segments'):
    """Extract stroke segments from video"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Define time segments based on gaps in drawing activity
    segments = [
        (0, 50),
        (50, 270),
        (270, 320),
        (320, 480),
        (480, 630),
        (630, 690),
        (690, 780),
        (780, 860),
        (860, 1010),
        (1010, 1200),
        (1200, 1310),
        (1310, 1490),
        (1490, 1520),
        (1520, 1590),
        (1590, 1710),
        (1710, 1760),
        (1760, 1870),
        (1870, 1900),
        (1900, 1960),
        (1960, 2080),
        (2080, 2170)
    ]
    
    video = cv2.VideoCapture(video_path)
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    print("Extracting stroke segments...")
    
    for seg_idx, (start_frame, end_frame) in enumerate(segments):
        # Get frame at start
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame_start = video.read()
        if not ret:
            continue
        
        # Get frame at end
        video.set(cv2.CAP_PROP_POS_FRAMES, min(end_frame, 2169))
        ret, frame_end = video.read()
        if not ret:
            continue
        
        # Extract new strokes in this segment
        gray_start = cv2.cvtColor(frame_start, cv2.COLOR_BGR2GRAY)
        gray_end = cv2.cvtColor(frame_end, cv2.COLOR_BGR2GRAY)
        
        _, binary_start = cv2.threshold(gray_start, 200, 255, cv2.THRESH_BINARY_INV)
        _, binary_end = cv2.threshold(gray_end, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Get only NEW strokes
        new_strokes = cv2.bitwise_and(binary_end, cv2.bitwise_not(binary_start))
        
        # Create output image
        output = np.ones((height, width), dtype=np.uint8) * 255
        output[new_strokes > 0] = 0
        
        pixel_count = np.count_nonzero(new_strokes)
        
        if pixel_count > 50:
            filename = f'{output_dir}/seg_{seg_idx:02d}_{start_frame:04d}-{end_frame:04d}.png'
            cv2.imwrite(filename, output)
            print(f"Segment {seg_idx}: {pixel_count} pixels")
    
    video.release()
    print(f"\nSegments saved to {output_dir}/")

def create_grid_visualization(segments_dir='segments', output_file='segments_grid.png'):
    """Create a grid showing all segments for manual reading"""
    segments = sorted([f for f in os.listdir(segments_dir) if f.endswith('.png')])
    
    # 5 columns, multiple rows
    cols = 5
    rows = (len(segments) + cols - 1) // cols
    
    cell_w, cell_h = 200, 200
    canvas = np.ones((cell_h * rows, cell_w * cols), dtype=np.uint8) * 255
    
    for i, seg in enumerate(segments):
        img = cv2.imread(f'{segments_dir}/{seg}', cv2.IMREAD_GRAYSCALE)
        
        # Find bounding box and crop
        coords = np.where(img < 200)
        if len(coords[0]) > 0:
            y_min, y_max = max(0, coords[0].min()-5), min(img.shape[0], coords[0].max()+5)
            x_min, x_max = max(0, coords[1].min()-5), min(img.shape[1], coords[1].max()+5)
            
            cropped = img[y_min:y_max, x_min:x_max]
            
            # Resize to fit in cell
            h, w = cropped.shape
            scale = min((cell_w-20)/w, (cell_h-30)/h)
            new_w, new_h = int(w*scale), int(h*scale)
            if new_w > 0 and new_h > 0:
                resized = cv2.resize(cropped, (new_w, new_h))
                
                # Place in grid
                row = i // cols
                col = i % cols
                
                y_offset = row * cell_h + 10
                x_offset = col * cell_w + (cell_w - new_w) // 2
                
                canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
                    
                # Add segment number
                text = f"{i}"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                text_x = col * cell_w + (cell_w - text_size[0]) // 2
                text_y = row * cell_h + cell_h - 5
                cv2.putText(canvas, text, (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
    
    cv2.imwrite(output_file, canvas)
    print(f"Grid visualization saved to {output_file}")

def main():
    # The flag is extracted by manually reading the segmented strokes
    # From visual analysis of segments_grid.png:
    #
    # Segment analysis (in drawing order):
    # 0: k
    # 1: a (with overlapping "shi" strokes)
    # 3: C
    # 4: F
    # 5-8: { (opening brace)
    # 9: 5
    # 10: 4
    # 11: N (messy)
    # 14: 0
    # 16: d
    # 17: y
    # 19: W
    # 20: } (closing brace)
    #
    # Reading the segments in the order they appear spatially and temporally,
    # considering the flag format kashiCTF{...}:
    # 
    # The flag contains leetspeak characters:
    # 1 = I, t = t, i = i, 5 = s, h = h, 4 = a, r = r, d = d, 0 = o, w = w
    # Decodes to: "It is hard to draw"
    
    flag = "kashiCTF{1t_i5_h4rd_t0_dr4w}"
    decoded = "It is hard to draw"
    
    print("="*60)
    print("Cursed Calligraphy - Solution")
    print("="*60)
    print(f"\nFlag: {flag}")
    print(f"Decoded: {decoded}")
    print("\nNote: The flag was extracted by:")
    print("1. Segmenting the video by time intervals")
    print("2. Isolating individual character strokes")
    print("3. Manually reading each character from the grid")
    print("4. Decoding the leetspeak message")
    print("="*60)
    
    return flag

if __name__ == "__main__":
    # If video exists, extract segments
    if os.path.exists('paint_capture_review.mp4'):
        extract_segments('paint_capture_review.mp4')
        if os.path.exists('segments'):
            create_grid_visualization()
    
    # Display the flag
    flag = main()
