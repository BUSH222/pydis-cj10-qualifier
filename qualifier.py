from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    dimx = image_size[0]/tile_size[0]
    dimy = image_size[1]/tile_size[1]
    if dimx.is_integer() and dimy.is_integer():
        if len(ordering) == dimx*dimy and len(ordering)-1 == max(ordering):
            print('passed')
            if set(range(max(ordering)+1)) == set(ordering):
                return True
    return False

def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size of ordering are not valid for the given image".
    """

    im = Image.open(image_path)
    if not valid_input(image_size=im.size, tile_size=tile_size, ordering=ordering):
        raise ValueError("The tile size of ordering are not valid for the given image")
    
    im_fin = Image.new("RGB", im.size, (255, 255, 255))

    dimx = im.size[0]/tile_size[0]
    dimy = im.size[1]/tile_size[1]

    print(dimx, dimy)

    for i, pos in enumerate(ordering):
        print(pos//2, pos%2, i, pos)
        #print(i % dimx, i//dimy)
        box = ((pos%2)*tile_size[0], (pos//2)*tile_size[1],\
                 (1+pos%2)*tile_size[0],  (1+pos//2)*tile_size[1])
        boxfin = tuple(map(int, ((i%dimx)*tile_size[0], (i//dimy)*tile_size[1],\
                 (1+ i%dimx)*tile_size[0], (1+i//dimy)*tile_size[1])))
        region = im.crop(box)
        im_fin.paste(region, boxfin)
    im_fin.show()
    im_fin.save(out_path)
