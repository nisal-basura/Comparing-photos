import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
import tkinter as tk
from tkinter import filedialog

class ImageComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Comparator")

        # Variables to store loaded images
        self.img1 = None
        self.img2 = None

        # Create buttons
        self.load_image1_button = tk.Button(root, text="Load Image 1", command=self.load_image1)
        self.load_image1_button.pack(pady=10)

        self.load_image2_button = tk.Button(root, text="Load Image 2", command=self.load_image2)
        self.load_image2_button.pack(pady=10)

        self.compare_button = tk.Button(root, text="Compare Images", command=self.compare_images)
        self.compare_button.pack(pady=20)

    def load_image1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img1 = cv2.imread(file_path)
            self.img1 = cv2.resize(self.img1, (600, 360))
            cv2.imshow("Image 1", self.img1)

    def load_image2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.img2 = cv2.imread(file_path)
            self.img2 = cv2.resize(self.img2, (600, 360))
            cv2.imshow("Image 2", self.img2)

    def compare_images(self):
        if self.img1 is not None and self.img2 is not None:
            gray1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)

            (similar, diff) = compare_ssim(gray1, gray2, full=True)

            diff = (diff * 255).astype("uint8")
            cv2.imshow("Difference", diff)

            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(self.img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(self.img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    cv2.putText(self.img2, "Similarity: {:.2f}".format(similar), (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2)

            x = np.zeros((360, 10, 3), np.uint8)
            result = np.hstack((self.img1, x, self.img2))
            cv2.imshow("Differences", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageComparatorApp(root)
    root.mainloop()
