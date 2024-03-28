import cv2
from skimage.metrics import structural_similarity as ssim
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
    similarity_index, _ = ssim(gray1, gray2, full=True)

    # Convert similarity index to percentage difference
    percentage_difference = (1 - similarity_index) * 100

    return percentage_difference

def open_file_dialog(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def calculate_difference(entry1, entry2, result_label):
    image_path1 = entry1.get()
    image_path2 = entry2.get()

    if image_path1 and image_path2:
        difference_percentage = compare_images(image_path1, image_path2)
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

    browse_button1 = tk.Button(root, text="Browse", command=lambda: open_file_dialog(entry1))
    browse_button2 = tk.Button(root, text="Browse", command=lambda: open_file_dialog(entry2))
    compare_button = tk.Button(root, text="Compare", command=lambda: calculate_difference(entry1, entry2, result_label))

    # Organize widgets using the grid layout
    label1.grid(row=0, column=0, padx=5, pady=5)
    entry1.grid(row=0, column=1, padx=5, pady=5)
    browse_button1.grid(row=0, column=2, padx=5, pady=5)

    label2.grid(row=1, column=0, padx=5, pady=5)
    entry2.grid(row=1, column=1, padx=5, pady=5)
    browse_button2.grid(row=1, column=2, padx=5, pady=5)

    compare_button.grid(row=2, column=1, pady=10)
    result_label.grid(row=3, column=0, columnspan=3)

    # Run the main loop
    root.mainloop()
