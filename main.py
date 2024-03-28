import cv2
from skimage.metrics import structural_similarity as ssim

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

if __name__ == "__main__":
    # Provide the paths to the two images you want to compare
    image_path1 = "path/to/image1.jpg"
    image_path2 = "path/to/image2.jpg"

    # Compare images and get the percentage difference
    difference_percentage = compare_images(image_path1, image_path2)

    # Print the result
    print(f"Percentage Difference: {difference_percentage:.2f}%")
