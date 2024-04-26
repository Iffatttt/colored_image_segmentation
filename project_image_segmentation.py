from PIL import Image
from disjoint_set_union import *
import requests
import os

def width_height_resized_image(image_path):
    # this function is resizing the image into lesser no. of pixels because its initial pixels takes a lot of time to run
    image = Image.open(image_path) #opens image
    width,height=image.size #gives width and height of pixels
    target_pixels=20000
    current_pixels=width*height
    # calculating new height and width
    ratio= (target_pixels / current_pixels) ** 0.5
    target_width=int(width * ratio) 
    target_height = int(height*ratio)
    return target_width,target_height

# width_height_resized_image(image_path)

def download_image_from_url(image_url, save_path):
    try:
        response = requests.get(image_url)
        # code is 200 if request successful
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully as {save_path}")
            return save_path  # Return the save path after successful download
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None  # Return None if download fails
    except Exception as e:
        print(f"An error occurred while downloading the image: {e}")
        return None  # Return None on error

def download_image_from_file(file_path):
    try:
        if os.path.exists(file_path):
            print(f"Using local image file: {file_path}")
            return file_path
        else:
            print(f"File not found: {file_path}")
            return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def save_user_image():
    user_input = input("Enter the image address or local file path (e.g: image.jpg) of the image you want to process: ")

    if user_input.startswith('http://') or user_input.startswith('https://'):
        # User input is a URL
        save_path = 'user_input.jpg'  # Specify local save path for downloaded image
        downloaded_path = download_image_from_url(user_input, save_path)
    else:
        # User input is a local file path
        downloaded_path = download_image_from_file(user_input)

    if downloaded_path:
        # Process the downloaded or local image
        target_width, target_height = width_height_resized_image(downloaded_path)
        resized_image = Image.open(downloaded_path).resize((target_width, target_height))
        resized_image.save('input.jpg')
    else:
        print("Image download or file read failed. Please try again.")

# Call the function to save and process the user-provided image
save_user_image()

def image_pixels(image_path):
# this function returns a list rgb tuples of every pixel
    resized_image=Image.open(image_path)
    resized_image.show()
    pixels=list(resized_image.getdata())#gives tuples of colour intensity of each pixel in a list
    return pixels

# image_pixels(image_path)

def initialize_dsu(image_path):
    # this fucntion calls the make set function of dsu to initialize sets in dsu where each node is a parent of itself
    dsu = {}
    target_width,target_height=width_height_resized_image(image_path)
    no_of_pixels=target_width*target_height
    dsu=make_set(no_of_pixels) 
    return dsu

def coordinates_dict(image_path):
# this function makes a dict where the keys are no. of pixel and the values are a tuple of its respective x,y coordinates 
    dsu_xy = {} 
    target_width,target_height=width_height_resized_image(image_path)
    for y in range(target_height):
        for x in range(target_width):
            node= y*target_width+x 
            dsu_xy[node]=(x,y) #the number of pixel is set as key and its x,y coordinates as value in dictionary of dsu
    return dsu_xy 

def threshold(image_path):
    # this function uses the union and find to find pixels that belong in the same segment/set 
    dsu = initialize_dsu(image_path) 
    dsu_xy = coordinates_dict(image_path)
    threshold_value = 25
    # the threshold_value is set to compare the rgb color intensity of one pixel with another
    pixels = image_pixels(image_path) 

    for pixel in range(len(dsu) - 1): 
        # root: the pixel we are using to compare
        root = find(dsu, pixel) 
        
        for pixel2 in range(pixel + 1, len(dsu) ):
            # this checks if pixel1 and pixel2 belongs in the same segment
            if abs(pixels[pixel][0] - pixels[pixel2][0]) <= threshold_value and \
               abs(pixels[pixel][1] - pixels[pixel2][1]) <= threshold_value and \
               abs(pixels[pixel][2] - pixels[pixel2][2]) <= threshold_value:
                
                # root2: the pixel we are comparing 
                root2=find(dsu,pixel2)
    
                # this merges the pixels that have the same rgb threshold 
                union(dsu, root, root2)
    return dsu

def segment_dsu(image_path):
    # this function makes the parent root the representative root of every pixel that belongs in a same segment 
    # returns a dict where key is the representative root and value is the list of all pixels that have the same threshold as the key pixel
    dsu = threshold(image_path)  
    segmented_dsu = {}
    for pixel, root in dsu.items():
        if root in segmented_dsu:
            segmented_dsu[root].append(pixel)
        else:
            segmented_dsu[root] = [pixel]
    return segmented_dsu
    #  the keys in segmented_dsu are the no.of segments the image is divided into

def no_of_segments(image_path):
    # the keys in segmented_dsu are the no.of segments the image is divided into
    segmented_dsu=segment_dsu(image_path)
    for i, v in segmented_dsu.items():  
        print("The segments in the image are pixel number:" ,i)

def rgb_dict(image_path):
    # this function creates a dict where keys are (x,y) of each pixel and values are its respective tuple
    pixels=image_pixels(image_path)
    dsu_rgb={}
    target_width,target_height=width_height_resized_image(image_path)
    for y in range(target_height):
        for x in range(target_width):
            dsu_rgb[(x,y)]=None #the  x,y coordinates as key in the dictionary
    index=0
    for i in dsu_rgb:
        dsu_rgb[i]=pixels[index] #and its respective rgb tuples as values
        index+=1
    return dsu_rgb

def rgb_segmentation_tuple(image_path):
# this function creates a dict where keys are coordinates and values are the rgb tuple of the segment it belongs to

# dsu: key node, value is list of pixels
    dsu=segment_dsu(image_path)
# dsu_xy:the number of pixel is set as key and its x,y coordinates as value in dictionary of dsu
    dsu_xy=coordinates_dict(image_path)
#  dsu_rgb:x,y coordinates as key in dictionary and its respective rgb tuples as values
    dsu_rgb=rgb_dict(image_path)

    segmented_rgb_tuples={}
# dsu: key node, value is list of pixels
    for parent_pixel, pixels in dsu.items(): 
        parent_rgb= dsu_rgb[dsu_xy[parent_pixel]]
        # assigning rgb tuple of parent pixel to a variable parent_rgb
        for pixel in pixels:
            cooridnates=dsu_xy[pixel]
# sets the parent rgb tuple to rgb tuple of pixels that belong in same segment
            segmented_rgb_tuples[cooridnates]=parent_rgb 
# segmented_rgb_tuples: keys are (x,y) coordinates and values are segmented rgb tuples
    return segmented_rgb_tuples

def create_segmented_image(image_path): 
# converts segemnted dsu of pixels into a segmented image
    segmented_rgb_tuples=rgb_segmentation_tuple(image_path)  
    target_width,target_height=width_height_resized_image(image_path)
    segmented_image=Image.new("RGB", (target_width,target_height)) 

    for cooridnates, rgbtuples in segmented_rgb_tuples.items():
        segmented_image.putpixel(cooridnates,rgbtuples) 

    segmented_image.save('output.jpg')
    segmented_image.show()




# test cases

# image_path="parrot2.jpg"

# image_path='flower.jpg'

# image_path='cheetah.jpg'

# image_path='parrot.jpg'

# image_path='carr.jpg'

# image_path='rabbit.jpg'


image_path='input.jpg'

image_pixels(image_path)
initialize_dsu(image_path)
coordinates_dict(image_path)
threshold(image_path)
segment_dsu(image_path)
no_of_segments(image_path)
rgb_dict(image_path)
rgb_segmentation_tuple(image_path)
create_segmented_image(image_path)






