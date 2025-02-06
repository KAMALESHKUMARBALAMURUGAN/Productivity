import cv2
import easyocr
import numpy as np
import sys

print("before")
# At the very beginning of your script:
sys.stdout.reconfigure(encoding='utf-8') # or sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

print("after")

def extract_circled_numbers(image_path):
    """
    Extracts circled numbers and their nearby numbers from an image.

    Args:
        image_path: Path to the input image.

    Returns:
        A dictionary where keys are the circled numbers and values are lists
        of their nearby numbers.  Returns an empty dictionary if no circled
        numbers are found or if there's an issue.
    """

    try:
        print("Entered try, Extracting circled numbers...")
        # 1. Load the image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Could not read image at {image_path}")
            return {}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY) # Adjust threshold as needed

        # 2. Detect circles (adjust parameters as needed)
        circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=10, maxRadius=40)  # Tune these!

        circled_numbers = {}

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            # 3. OCR (using easyocr)
            reader = easyocr.Reader(['en'])  # You might need to specify languages

            for (x, y, r) in circles:
                # Crop the circle region
                x1 = max(0, x - r)
                y1 = max(0, y - r)
                x2 = min(img.shape[1], x + r)
                y2 = min(img.shape[0], y + r)
                circle_roi = img[y1:y2, x1:x2]

                # Perform OCR on the circled region
                result = reader.readtext(circle_roi)
                print("Result: ", result)

                circled_num = None
                for detection in result:
                    text, confidence, _ = detection
                    try:
                        circled_num = int(text)  # Try to convert to integer
                        break  # Stop if a number is found
                    except ValueError:
                        pass  # Ignore non-numbers

                if circled_num is not None:
                    circled_numbers[circled_num] = []

                    # 4. Find nearby numbers (this part needs refinement)
                    # (This is a simplified approach; you might need to adjust the 
                    #  search area and criteria based on your image layout)
                    search_x1 = max(0, x - 75)  # Adjust search radius
                    search_y1 = max(0, y - 75)
                    search_x2 = min(img.shape[1], x + 75)
                    search_y2 = min(img.shape[0], y + 75)
                    search_roi = img[search_y1:search_y2, search_x1:search_x2]
                    nearby_result = reader.readtext(search_roi)

                    for nearby_detection in nearby_result:
                        # nearby_text, nearby_conf, _ = nearby_detection
                        nearby_text = nearby_detection[1]
                        if isinstance(nearby_text, list):  # Check if it is a list
                            nearby_text = " ".join(nearby_text) # Join them to a string
                        try:
                            nearby_num = int(nearby_text)
                            if nearby_num != circled_num: # Avoid self-matching
                                circled_numbers[circled_num].append(nearby_num)
                        except ValueError:
                            pass

        return circled_numbers
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}



# Example usage:
image_path = r"C:\Users\kamalesh.kb\KAMALESH_PRODUCTIVITY\Productivity\input_file.jpg"  # Replace with the actual path to your image
result = extract_circled_numbers(image_path)

if result:
    for circled_num, nearby_nums in result.items():
        print(f"Circled Number: {circled_num}, Nearby Numbers: {nearby_nums}")
else:
    print("No circled numbers found or an error occurred.")