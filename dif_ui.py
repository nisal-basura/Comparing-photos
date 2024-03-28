import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import tkinter as tk
from tkinter import filedialog

def compare_images(image1, image2):
    # Read the images
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute Structural Similarity Index (SSI)
    similarity_index, diff_map = ssim(gray1, gray2, full=True)

    # Convert the difference map to a binary mask
    threshold = 0.05  # Adjust this threshold as needed
    diff_mask = (diff_map > threshold).astype("uint8") * 255

    # Find contours in the difference mask
    contours, _ = cv2.findContours(diff_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around differing regions on both images
    img_diff1 = img1.copy()
    img_diff2 = img2.copy()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img_diff1, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangles
        cv2.rectangle(img_diff2, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangles

    # Combine the two images horizontally
    combined_image = np.hstack((img_diff1, img_diff2))

    return combined_image, (1 - similarity_index) * 100

def open_file_dialog(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def calculate_difference(entry1, entry2, result_label, image_label):
    image_path1 = entry1.get()
    image_path2 = entry2.get()

    if image_path1 and image_path2:
        # Compare images and get the combined image with differences highlighted
        combined_image, difference_percentage = compare_images(image_path1, image_path2)

        # Display the combined image with differences
        cv2.imshow("Differences", combined_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Update the result label with the percentage difference
        result_label.config(text=f"Percentage Difference: {difference_percentage:.2f}%")
    else:
        result_label.config(text="Please select both images.")

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Image Comparison")

    # Create entry widgets for image paths
    entry1 = tk.Entry(root, width=40)
    entry2 = tk.Entry(root, width=40)

    # Create labels and buttons
    label1 = tk.Label(root, text="Image 1:")
    label2 = tk.Label(root, text="Image 2:")
    result_label = tk.Label(root, text="Percentage Difference: ")
    image_label = tk.Label(root, text="Differences:")

    browse_button1 = tk.Button(root, text="Browse", command=lambda: open_file_dialog(entry1))
    browse_button2 = tk.Button(root, text="Browse", command=lambda: open_file_dialog(entry2))
    compare_button = tk.Button(root, text="Compare", command=lambda: calculate_difference(entry1, entry2, result_label, image_label))

    # Organize widgets using the grid layout
    label1.grid(row=0, column=0, padx=5, pady=5)
    entry1.grid(row=0, column=1, padx=5, pady=5)
    browse_button1.grid(row=0, column=2, padx=5, pady=5)

    label2.grid(row=1, column=0, padx=5, pady=5)
    entry2.grid(row=1, column=1, padx=5, pady=5)
    browse_button2.grid(row=1, column=2, padx=5, pady=5)

    compare_button.grid(row=2, column=1, pady=10)
    result_label.grid(row=3, column=0, columnspan=3)
    image_label.grid(row=4, column=0, columnspan=3)

    # Run the main loop
    root.mainloop()
