# Seth's "twins" from thispersondoesnotexist.com

Searching for the Seth Macfarlane's twins on https://thispersondoesnotexist.com 

![](https://www.biography.com/.image/c_fill,cs_srgb,dpr_1.0,g_face,h_300,q_80,w_300/MTE1ODA0OTcxOTI3NzAxMDA1/seth-macfarlane-20624525-1-402.jpg)

Of course you can search twin for any other person :)


## Installation
```
git clone https://github.com/Radg/seth-twin-search.git 
cd set-twin-search
chmod +x face.py
```

## Requirements

You'll need API key and secret from http://faceplusplus.com

```APIKEY = "*********"```

```APISEC = "*********"```

You will also need API URLs based on your location.

IMG_URL is a url for image with desired person. Image must contain only one face.

```IMG_URL = path_to_seth_image```


## Usage

```./face.py -c 62 -n 100```

where:

`	-c` - "Similarity" level (0..100), above 70 is good

`	-n` - number of images needed


## Credits

Based on https://github.com/neoncloud/Find_your_face script.
